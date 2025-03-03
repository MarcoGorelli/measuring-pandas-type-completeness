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
7. Run `pyright --verifytypes pandas --ignoreexternal --outputjson > type_report.json`
8. Install `marimo edit analysis.py`.

Notes:
- There's a lot of false positives because `Series` is often used internally
  in pandas-stubs as opposed to `Series[Any]`. Issue: https://github.com/pandas-dev/pandas-stubs/issues/1133
- PyRight includes all exported modules, including those that pandas considers private. Examples are:
  - `base` files (contain objects meant to be subclassed and are not directly user-facing)
  - `tests` (definitely not user-facing)

Once pandas-stubs #1133 is addressed, then the report may be more useful. Currently,
it is riddled with "type is unknown" just because the generic type of `Series` is not
specified. However, the `analysis.py` file does at least give us the means to find
public-facing methods where type annotations are missing completely.

