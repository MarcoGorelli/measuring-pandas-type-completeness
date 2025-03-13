# Measure pandas' type completeness

Here's a utility for measuring pandas' type-completeness.

Usage:
1. Make sure you have Python3.12 installed
2. `python3.12 -m venv .venv`. I'd suggest not using `uv`, because `uv`
   does some clever caching, and here you'll be adding files to your
   local site packages.
3. Clone `pandas-stubs` from `https://github.com/pandas-dev/pandas-stubs`
4. Install pandas nightly. See https://pandas.pydata.org/docs/getting_started/install.html
   for how to do that.
5. Run `python inline_pandas_stubs.py` with your virtual environment activated.
6. Install `pyright` and `marimo` into your virtual environment.
7. Run `git clone https://github.com/pandas-dev/pandas.git pandas-dev --depth=1`
8. Run `python list_public_methods.py`. This will generate `public_methods.csv` with
   the public  methods from the pandas API.
7. Run `pyright --verifytypes pandas --ignoreexternal --outputjson > type_report.json`
8. Run `marimo edit analysis.py`.

At the end of the Marimo notebook, there's a cell showing which public functions
in pandas has missing types.

Limitations:
- StringMethods (e.g. `Series.str.upper`) are incorrectly flagged as "type unknown"

