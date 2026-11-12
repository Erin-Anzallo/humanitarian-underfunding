"""Functions used in several notebooks of the project.

Generated with Claude (Anthropic): find the repository folder and read
World Bank DataBank CSV exports into a long country-year table.
"""
import os
from pathlib import Path

import pandas as pd


def find_root():
    """Find the repository folder (the one containing data/raw and code/),
    whatever folder Jupyter started the kernel in."""
    def is_root(folder):
        return (folder / "data" / "raw").is_dir() and (folder / "code").is_dir()

    starts = []
    notebook = os.environ.get("JPY_SESSION_NAME")  # path of the notebook, set by JupyterLab
    if notebook:
        starts.append(Path(notebook).resolve().parent)
    starts.append(Path.cwd())

    # 1. The start folder or one of its parents
    for start in starts:
        for folder in [start, *start.parents]:
            if is_root(folder):
                return folder

    # 2. Subfolders of the current folder, up to two levels down
    cwd = Path.cwd()
    for folder in [*cwd.glob("*"), *cwd.glob("*/*")]:
        if folder.is_dir() and is_root(folder):
            return folder

    raise FileNotFoundError(
        "Repository folder not found: open the notebook from the code/ folder.")


def read_worldbank(path):
    """Read a World Bank DataBank CSV export (years in columns) and return a
    long table with one row per country, year and series:
    countryCode, year, series, value."""
    df = pd.read_csv(path)

    # The last lines of the export are notes, with no series code: drop them
    df = df.dropna(subset=["Series Code"])

    # Year columns look like "2010 [YR2010]"
    year_cols = [c for c in df.columns if c[:4].isdigit()]
    long = df.melt(id_vars=["Country Code", "Series Code"], value_vars=year_cols,
                   var_name="year", value_name="value")

    long["year"] = long["year"].str[:4].astype(int)
    # Missing values are written ".." in DataBank exports
    long["value"] = pd.to_numeric(long["value"].replace("..", pd.NA), errors="coerce")
    return long.rename(columns={"Country Code": "countryCode",
                                "Series Code": "series"})


def country_folds(df, n_folds=5):
    """Assign each row to one of n_folds cross-validation folds, keeping all
    rows of a country in the same fold (GroupKFold). The same function is used
    for the logistic regression and the gradient boosting, so both models are
    evaluated on exactly the same folds."""
    from sklearn.model_selection import GroupKFold
    folds = pd.Series(-1, index=df.index)
    splitter = GroupKFold(n_splits=n_folds)
    for k, (_, test) in enumerate(splitter.split(df, groups=df["countryCode"])):
        folds.iloc[test] = k
    return folds.to_numpy()