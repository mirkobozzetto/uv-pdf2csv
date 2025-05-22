# uv-pdf2csv

Minimal CLI tool to convert any PDF with tables into a CSV.

## Install (macOS, Python 3)

```bash
uv add fastapi uvicorn tabula-py pandas python-multipart
```

– installs FastAPI, Uvicorn (ASGI server), Tabula-Py (PDF→CSV), Pandas and multipart support via UV ([Medium][1]).

## Usage

Make sure your script is executable:

```bash
chmod +x main.py
```

Then run:

```bash
./main.py <input.pdf>
```

Behind the scenes it uses Tabula-Py in lattice mode to detect table borders and export clean CSVs ([tabula-py.readthedocs.io][2], [pypi.org][3]).

[1]: https://medium.com/%40gnetkov/start-using-uv-python-package-manager-for-better-dependency-management-183e7e428760 "Start Using UV Python Package Manager for Better Dependency ..."
[2]: https://tabula-py.readthedocs.io/en/latest "Getting Started — tabula-py documentation"
[3]: https://pypi.org/project/tabula-py "tabula-py - PyPI"
