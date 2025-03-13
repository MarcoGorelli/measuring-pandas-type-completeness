import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    with open("type_report.json") as fd:
        type_report = json.load(fd)
    return fd, json, type_report


@app.cell
def _(type_report):
    import polars as pl
    import duckdb

    symbols = type_report["typeCompleteness"]["symbols"]
    df = (
        pl.DataFrame(symbols)
        .filter(
            pl.col("isExported"),
            ~pl.col("name").str.starts_with("pandas.tests"),
            ~pl.col("name").str.starts_with("pandas.core.internals"),
        )
        .drop("isExported")
        .with_columns(
            pl.col("diagnostics").cast(pl.List(pl.String)).list.join(",")
        )
        .with_columns(
            alternateNames=pl.concat_list(
                pl.col("alternateNames").fill_null(pl.lit([])),
                pl.concat_list("name"),
            )
        )
        .drop("isTypeAmbiguous")
        .with_columns(
            pl.col("alternateNames").list.eval(
                pl.element().str.strip_prefix("pandas.core.frame.")
            ),
        )
        .with_columns(
            pl.col("alternateNames").list.eval(
                pl.element().str.strip_prefix("pandas.core.series.")
            ),
        )
        .with_columns(name=pl.col("alternateNames").list.first())
    )
    return df, duckdb, pl, symbols


@app.cell
def _(df, pl):
    df.filter(pl.col("alternateNames").list.join(",").str.contains("set_axis"))
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    with open("public_methods.csv") as _fd:
        public_methods = _fd.read().splitlines(keepends=False)
    return (public_methods,)


@app.cell
def _(df, pl, public_methods):
    public_df = df.filter(
        pl.col("alternateNames")
        .list.eval(pl.element().is_in(public_methods))
        .list.any(),
        ~pl.col("category").is_in(["class", "variable"]),
    )
    public_df.head()
    return (public_df,)


@app.cell
def _(pl, public_df):
    public_df.filter(~pl.col("isTypeKnown")).drop("diagnostics")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
