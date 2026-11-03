# Dialog

A local trading-research desk with two competing research approaches, an independent evaluator, and one shared paper portfolio.

Dialog uses Python, the public Adaptive Research Harness client, and LangGraph. The browser workspace shows investigations, rejected ideas, strategies, positions, research spending, execution costs, and decisions needing attention.

## Run locally

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python scripts/install_arh_client.py
.venv/bin/python run.py --port 8787
```

Keep ARH checked out at the commit in [arh-dependency.json](arh-dependency.json). Set `DIALOG_ARH_ROOT` if its location differs from `/Users/jedgore/dev/speedway`.

Open **http://127.0.0.1:8787/**. Choose **Run two cycles** to follow the complete example, or **Next step** to inspect each transition. Then choose **Advance to scheduled exits** to close the remaining positions.

The example includes a rejected approach, revised research, shared allocation, partial fills, a lost order response, interrupted researchers, and recovery. All observations and trades are synthetic. Research units are accounted for separately from paper capital.

## Read and verify

- [Operating guide](APP.md)
- [Current implementation and rename record](validation/dialog/REPORT.md)
- [ARH consumer validation](validation/v01_integrated_m1/REPORT.md)
- [Design contracts](docs/contracts.md)

```sh
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```
