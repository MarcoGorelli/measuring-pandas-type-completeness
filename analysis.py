import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    with open("type_report.json") as fd:
        content = json.load(fd)
    return content, fd, json


@app.cell
def _(content):
    import polars as pl
    import duckdb

    symbols = content["typeCompleteness"]["symbols"]
    df = pl.DataFrame(symbols).with_columns(
        pl.col("diagnostics").cast(pl.List(pl.String)).list.join(",")
    )
    return df, duckdb, pl, symbols


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _():
    with open("public_methods.csv") as _fd:
        content_list = _fd.read().splitlines(keepends=False)
    public_methods = " or ".join([f"name like '%.{x}'" for x in content_list])
    public_methods[:100]
    return content_list, public_methods


@app.cell
def _(df, duckdb, public_methods):
    duckdb.sql(f"""
    from df lhs
    select name
    -- anything in base in meant to be subclassed
    where ({public_methods})
    and name not like '%tests%'
    and name not like '%plotting%'
    and name not like '%internals%'
    and category != 'variable'
    and isExported
    and not isTypeKnown
    and diagnostics like '% is missing%'
    """)
    return


@app.cell
def _(df, duckdb, public_methods):
    duckdb.sql(f"""
    from df
    select avg(cast(isTypeKnown as int64))
    -- anything in base in meant to be subclassed
    where ({public_methods})
    and name not like '%tests%'
    and name not like '%plotting%'
    and name not like '%internals%'
    and category != 'variable'
    and isExported
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
