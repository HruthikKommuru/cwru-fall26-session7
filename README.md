# Python Foundations for AI Systems

Case Western Reserve University · Fall 2026 · Session 7

Start here if you know a little Python and are new to language-model apps.
Five short notebooks build from environments and functions to handling messy
model replies and wrapping a weather API. No model subscription or API key is needed.
Use Python 3.10 or newer. Examples work on macOS, Linux, Windows, and Colab.

## Setup in three steps

First clone this repository (or download and unzip it), open a terminal inside it,
then follow these three steps:

1. Create an isolated Python environment:
   ```bash
   python -m venv .venv
   ```
2. Activate it:
   ```bash
   source .venv/bin/activate
   ```
   On Windows PowerShell: `.venv\Scripts\Activate.ps1`.
   On Windows Command Prompt: `.venv\Scripts\activate`.
3. Install the workshop libraries and start the notebook app:
   ```bash
   pip install -r requirements.txt
   jupyter notebook
   ```

Open `notebooks/01_environment_setup.ipynb` and run cells from top to bottom.
For the name demo, copy `.env.example` to `.env` and change `your-name-here`.
Never commit `.env` or a secret. The supplied example contains no secret.

## Workshop notebooks

| Part | Notebook | Run in your browser |
| --- | --- | --- |
| 1 | [Environment setup](notebooks/01_environment_setup.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HruthikKommuru/cwru-fall26-session7/blob/main/notebooks/01_environment_setup.ipynb) |
| 2 | [Python essentials](notebooks/02_python_essentials.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HruthikKommuru/cwru-fall26-session7/blob/main/notebooks/02_python_essentials.ipynb) |
| 3 | [Data structures and model replies](notebooks/03_data_structures.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HruthikKommuru/cwru-fall26-session7/blob/main/notebooks/03_data_structures.ipynb) |
| 4 | [Errors, retries, and logging](notebooks/04_errors_and_logging.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HruthikKommuru/cwru-fall26-session7/blob/main/notebooks/04_errors_and_logging.ipynb) |
| 5 | [A weather tool wrapper](notebooks/05_tool_wrapper.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HruthikKommuru/cwru-fall26-session7/blob/main/notebooks/05_tool_wrapper.ipynb) |

Colab needs no local setup. Each notebook installs missing small libraries and
downloads the starter files automatically if the repository is absent.
Colab has its own Python environment; local activation commands are explanations,
not commands to run in a Colab cell. Internet is needed for that first download
and the weather examples. Most other examples work offline after installation.

Each lab starts with `# TODO` code. Fill it in, then run **Check yourself**.
An unfinished lab prints a reminder so you can still explore later sections.
Its assertions run after you replace the `None` placeholders.
For a worked answer, run `%run solutions/lab1.py` (change the number as needed)
in a new code cell immediately before the matching check. Notebook setup changes
the working directory to the repository root, so this works from any notebook.
The two deliberately failing cells are clearly labelled. In Part 1, IPython's
`!python` reports a failing subprocess in text rather than raising a notebook error;
the next cell shows the same error directly as a Python exception.

## Starter files

- `starter/hello.py`: print a greeting and the Python executable path.
- `starter/broken.py`: read a deliberate traceback (the error is on line 9).
- `starter/replies.py`: five messy model replies to practise parsing.
- `starter/flaky_api.py`: a pretend service that sometimes times out.
- `.env.example`: a safe name-setting example.
- `solutions/lab1.py` through `solutions/lab5.py`: worked answers.

Part 2 creates `tools.py` and `lab_tools.py` as practice; these are ignored by Git.
All generated execution copies and verification reports go in `output/`.
Each retry example caps the work at three attempts. The teaching loop waits after
each timeout, including the final one; production code can skip that last wait.

## Instructor verification

```bash
python scripts/verify.py
```

This runs each notebook with `jupyter nbconvert --to notebook --execute --allow-errors`,
then inspects every error. It checks both untouched student versions and versions
with the worked answers inserted. It also checks short cells, markdown explanations,
expected exceptions, exercise assertions, and the absence of saved outputs.
It writes `output/verification.json` and clears original notebook outputs using
`jupyter nbconvert --clear-output --inplace` before the final cleanliness check.
Do not interpret `--allow-errors` alone as a successful verification.

The lab's failure checks simulate known responses so they are stable even when
the network changes. Live weather results and connectivity are recorded separately.
See [Open-Meteo forecast docs](https://open-meteo.com/en/docs) and
[geocoding docs](https://open-meteo.com/en/docs/geocoding-api).
Weather data: Open-Meteo; location data: GeoNames, via Open-Meteo.
