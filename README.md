# Humanitarian underfunding: sector or country?

Advanced Data Analytics, HEC Lausanne, autumn 2026. Author: Erin Anzallo.

Humanitarian organisations often warn that some sectors, such as education and protection,
are chronically underfunded. This project tests whether the underfunding of UN humanitarian
appeals depends more on the sector or on the characteristics of the country (GDP per capita,
government effectiveness, humanitarian attention), using a logistic regression compared with
gradient boosting.

## How to run

1. Install the packages:
   ```
   pip install -r requirements.txt
   ```
2. Run the notebooks in `code/` in this order, each from top to bottom:

   | Notebook | What it does |
   |---|---|
   | `01_get_data.ipynb` | Downloads the number of ReliefWeb reports per country and year (see below) |
   | `02_clean.ipynb` | Cleans the OCHA data, merges country characteristics (t−1) and saves the analysis table |
   | `03_explore.ipynb` | Descriptive statistics and figures: funding rate, underfunding by sector, over time and by quintile of country characteristics |
   | `04_logistic_regression.ipynb` | Logistic regressions (sector vs country characteristics), marginal effects, country-grouped cross-validation|
   | `05_gradient_boosting.ipynb` | TODO |

All notebooks run in the Nuvolos workspace. Approximate running time: TODO.

### ReliefWeb appname

The ReliefWeb counts are already saved in `data/raw/reliefweb_counts.csv`, so all notebooks
run without any API access: without an appname, `01_get_data.ipynb` simply uses the saved file.

To download the counts again, you need a ReliefWeb API appname (request one at
https://reliefweb.int/help/api). Create a file `.env` at the root of the repository containing:

```
RELIEFWEB_APPNAME=your_appname
```

This file is listed in `.gitignore` and is never committed.

## Data

All raw data are in `data/raw/` and are never modified by hand.

| File | Source | Content | Downloaded | Licence |
|---|---|---|---|---|
| `fts_globalcluster.csv` | OCHA Financial Tracking Service, via the Humanitarian Data Exchange (HDX), dataset "Global – Requirements and Funding Data", file `fts_requirements_funding_globalcluster_global.csv` | Requirements and funding of UN humanitarian appeals by global cluster (sector), country and year | 11 November 2026 | CC BY-IGO |
| `wgi.csv` | World Bank, Worldwide Governance Indicators (DataBank) | Government Effectiveness: Estimate; Control of Corruption: Estimate; all countries | 11 November 2026 | CC BY 4.0 |
| `wdi_gdppc.csv` | World Bank, World Development Indicators (DataBank) | GDP per capita (constant 2015 US$); all countries | 11 November 2026 | CC BY 4.0 |
| `reliefweb_counts.csv` | ReliefWeb API (UN OCHA), produced by `code/01_get_data.ipynb` | Number of reports per primary country and year, 1999–2025 | 11 November 2026 | Derived counts |

## Repository structure

```
code/             notebooks, one per stage, and helpers.py
data/raw/         raw data (see above)
data/processed/   cleaned data produced by the notebooks
figures/          figures and tables used in the paper
paper.pdf         research paper (TODO)
```

## Licence

Code: MIT licence (see `LICENSE`). Data: see the licence of each source in the table above.
