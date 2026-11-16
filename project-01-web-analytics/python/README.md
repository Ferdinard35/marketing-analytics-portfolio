<!-- markdownlint-disable MD013 -->
# Python

Three scripts, run in order from this folder. They need Python 3.10 or later with the packages in [../requirements.txt](../requirements.txt) (pandas and matplotlib).

```powershell
python 01_clean_and_model.py            # about 10 seconds
python 02_analysis.py
python 03_verify_sql_against_python.py
```

| Script | What it does | Writes |
| --- | --- | --- |
| [01_clean_and_model.py](01_clean_and_model.py) | Removes duplicate events, standardises traffic labels, assigns channels, rebuilds sessions from events, and removes bots and internal traffic. Logs how many rows each step touched | `../data/cleaned/`, `../data/cediflow_web.db` |
| [02_analysis.py](02_analysis.py) | Builds one table per business question, runs a two-proportion z-test on each comparison the findings rest on, sizes each recommendation, and draws the charts | [output/](output/), [figures/](figures/) |
| [03_verify_sql_against_python.py](03_verify_sql_against_python.py) | Runs every query in `../sql/` and checks it against the pandas tables | `../sql/results/` |

`output/findings.json` holds every headline number, test result and estimate quoted in the project README and the executive report.

The significance tests are written out by hand in `02_analysis.py` (pooled standard error for the test, unpooled for the 95% interval) so the script has no dependency on scipy.
