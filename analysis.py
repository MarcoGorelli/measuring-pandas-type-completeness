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

    symbols = type_report["typeCompleteness"]["symbols"]
    symbols_df = pl.DataFrame(symbols)
    return pl, symbols, symbols_df


@app.cell
def _(rel, symbols_df):
    import duckdb

    rel = duckdb.sql("""
    from symbols_df
    select
        * exclude(isTypeAmbiguous, referenceCount, isExported, alternateNames, name),
        list_concat(list_value(name), ifnull(alternateNames, [])) as alternateNames
    where
        isExported
        and not starts_with(name, 'pandas.tests')
        and not starts_with(name, 'pandas.core.internals')
        and not starts_with(name, 'pandas.util')
        and category not in ('class', 'variable')
    """)
    rel = duckdb.sql(r"""
    from rel
    select
        * exclude (alternateNames),
        [regexp_replace(x, '^(pandas\.core\.frame|pandas\.core\.series)\.', '') for x in alternateNames] as alternateNames
    """)
    rel = duckdb.sql("""
    from rel
    select
        *,
        list_first(alternateNames) as name
    """)
    rel
    return duckdb, rel


@app.cell
def _():
    with open("public_methods.csv") as _fd:
        public_methods = _fd.read().splitlines(keepends=False)
    return (public_methods,)


@app.cell
def _(public_methods):
    public_methods[:10]
    return


@app.cell
def _(duckdb, public_methods, rel):
    public_rel = duckdb.sql(f"""
    from rel
    select *
    where list_bool_or([x in ({",".join([f"'{x}'" for x in public_methods])}) for x in alternateNames])
    """)
    return (public_rel,)


@app.cell
def _(duckdb, public_rel):
    duckdb.sql(
        """
        from public_rel
        select * exclude(diagnostics)
        where not isTypeKnown
        """
    ).pl()
    return


@app.cell
def _(symbols):
    [x for x in symbols if "Series.mean" in x["name"]]
    return


@app.cell
def _(duckdb, public_rel):
    duckdb.sql(
        """
        from public_rel
        select mean(cast(isTypeKnown as int64))
        """
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
