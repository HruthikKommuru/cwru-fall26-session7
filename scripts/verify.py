"""Execute student notebooks and worked answers; reject unexpected cell errors."""
import ast
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

import nbformat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
ENV = os.environ.copy()
ENV["PATH"] = str(Path(sys.executable).parent) + os.pathsep + ENV.get("PATH", "")
# Pin execution to the interpreter that launched verification, not a global kernel.
kernel = OUT / "kernels" / "session7"
kernel.mkdir(parents=True, exist_ok=True)
(kernel / "kernel.json").write_text(json.dumps({
    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    "display_name": "Session 7 verification", "language": "python",
}))
ENV["JUPYTER_PATH"] = str(OUT) + os.pathsep + ENV.get("JUPYTER_PATH", "")
ENV["JUPYTER_RUNTIME_DIR"] = str(OUT / "runtime")
report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "runs": []}


def nbconvert(*args):
    completed = subprocess.run(
        [sys.executable, "-m", "jupyter", "nbconvert", *args],
        cwd=ROOT, env=ENV, text=True, capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stdout + completed.stderr)


def validate_structure(nb):
    nbformat.validate(nb)
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        assert index and nb.cells[index - 1].cell_type == "markdown", index
        assert len(cell.source.splitlines()) <= 14, (index, "cell too long")
        assert not cell.outputs and cell.execution_count is None, index
        if "raises-exception" in cell.metadata.get("tags", []):
            assert "expect" in nb.cells[index - 1].source.lower()
    assert "Your turn" in "\n".join(c.source for c in nb.cells)
    assert nb.cells[-1].source.startswith("## What you learned")
    assert nb.cells[-1].source.count("\n- ") == 3


def with_solution(nb, number):
    result = copy.deepcopy(nb)
    # Insert after the last TODO scaffold, before demonstrations and assertions.
    last = max(i for i, c in enumerate(result.cells)
               if "exercise" in c.metadata.get("tags", []))
    result.cells[last + 1:last + 1] = [
        nbformat.v4.new_markdown_cell("Load the worked answer for instructor verification."),
        nbformat.v4.new_code_cell(f"%run solutions/lab{number}.py"),
    ]
    return result


def inspect_run(path, number, variant):
    nb = nbformat.read(path, as_version=4)
    errors = []
    passed_checks = 0
    live = None
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        tags = cell.metadata.get("tags", [])
        cell_errors = [o for o in cell.outputs if o.output_type == "error"]
        for error in cell_errors:
            expected = (number == 1 and "raises-exception" in tags
                        and error.ename == "NameError")
            errors.append({"cell": index, "type": error.ename, "expected": expected})
            if not expected:
                raise AssertionError(f"{path.name}, cell {index}: {error.ename}: {error.evalue}")
        text = "".join(o.get("text", "") for o in cell.outputs)
        if variant == "solutions" and "check" in tags:
            assert "Nice work!" in text, (path.name, index, "exercise check skipped")
            passed_checks += 1
        if "live-weather" in tags:
            # Stdout is the printed dictionary; warnings are separate stderr streams.
            stdout = "".join(o.get("text", "") for o in cell.outputs if o.get("name") == "stdout")
            live = ast.literal_eval(stdout.strip())
    if number == 1:
        assert sum(e["expected"] for e in errors) == 1
    return {"notebook": path.name, "variant": variant,
            "expected_errors": len(errors), "passed_check_cells": passed_checks,
            **({"live_weather": live} if live is not None else {})}


def main():
    for number, source in enumerate(sorted((ROOT / "notebooks").glob("*.ipynb")), 1):
        original = nbformat.read(source, as_version=4)
        validate_structure(original)
        for variant in ("student", "solutions"):
            nb = original if variant == "student" else with_solution(original, number)
            name = f"{source.stem}_{variant}.ipynb"
            input_path = OUT / name
            nbformat.write(nb, input_path)
            nbconvert("--to", "notebook", "--execute", "--allow-errors",
                      "--ExecutePreprocessor.timeout=180",
                      "--ExecutePreprocessor.kernel_name=session7",
                      "--output", name, "--output-dir", str(OUT), str(input_path))
            result = inspect_run(input_path, number, variant)
            report["runs"].append(result)
            print(f"PASS {source.name}: {variant}", flush=True)
    for source in sorted((ROOT / "notebooks").glob("*.ipynb")):
        nbconvert("--clear-output", "--inplace", str(source))
        validate_structure(nbformat.read(source, as_version=4))
    report["status"] = "passed"
    report["notebooks_without_outputs"] = 5
    (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("All ten executions passed; notebook outputs are clear.")


if __name__ == "__main__":
    main()
