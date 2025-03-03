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
    df
    return


@app.cell
def _(df, duckdb):
    duckdb.sql("""
    from df
    select avg(cast(isTypeKnown as int64))
    where name not like 'pandas.%.base.%'
    and name not like 'pandas.tests.%'
    and isExported
    """)
    return


@app.cell
def _(df, duckdb):
    duckdb.sql("""
    from df
    select name
    -- anything in base in meant to be subclassed
    where name not like 'pandas.%.base.%'
    -- ignore tests
    and name not like 'pandas.tests.%'
    and isExported
    and not isTypeKnown
    and diagnostics like '% is missing%'
    """).pl()
    return


@app.cell
def _(symbols):
    [x for x in symbols if "DataFrame.insert" in x["name"]]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
