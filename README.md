# Dark Fleets: Predicting Prolonged AIS Disabling Events

**Machine learning on global vessel-tracking data to flag fishing boats that "go dark" for long periods, a key warning sign of illegal fishing.**

Commercial fishing vessels broadcast their position through the Automatic Identification System (AIS). When a vessel switches its transponder off, it disappears from monitoring, and long, deliberate gaps are strongly associated with **Illegal, Unreported and Unregulated (IUU) fishing**. This project analyses more than 55,000 suspected disabling events worldwide and predicts which gaps will be **prolonged (24 hours or more)**.

## Data

| Dataset | Source | Use |
| --- | --- | --- |
| AIS disabling events | Global Fishing Watch, *Welch et al. (2022), "Hotspots of unseen fishing vessels"* | Where and when vessels went dark and reappeared, plus vessel class, flag, length and tonnage |
| Exclusive Economic Zones (EEZ v12) | Marine Regions (Flanders Marine Institute) | Maritime boundaries, used to engineer geospatial features |

The data isn't included in this repo. Download both from the sources above and place the CSV and the EEZ shapefile in the project folder (see `dataset_exploration.ipynb`).

## Approach

1. **Exploration and cleaning:** profiling, handling missing flags, encoding categorical fields (vessel class, flag state).
2. **Geospatial feature engineering:** spatial joins with GeoPandas to work out whether each gap started and ended **inside an EEZ**, plus distance to the nearest EEZ boundary and changes in distance from shore.
3. **Exploratory modelling:** K-Means clustering of where vessels go dark reveals global hotspots; a linear regression checks how distance from shore at the start of a gap relates to the end (R² ≈ 0.79).
4. **Classification:** an **XGBoost** model predicts whether a gap will last 24 hours or more, using an 80/20 stratified train/test split on a near-balanced target (49% prolonged).

## Results

| Class | Precision | Recall | F1 |
| --- | --- | --- | --- |
| Normal (< 24h) | 0.72 | 0.82 | 0.77 |
| Prolonged (≥ 24h) | 0.79 | 0.67 | 0.73 |
| **Overall accuracy** | | | **0.75** |

The notebook includes the confusion matrix and feature-importance analysis.

## Limitations and next steps

- **Data leakage:** some features, such as end position and distance travelled, are only known once a gap *ends*, so this model explains gaps after the fact rather than predicting them in real time. A true early-warning model should use only information available when the signal is lost.
- Add sequence models (e.g. an LSTM) over each vessel's movement before it goes dark.
- Tune hyperparameters and validate across regions and time periods to check the model generalises.

## Files

```
dataset_exploration.ipynb   # loading and first look at both datasets
dark_fleets_analysis.ipynb  # EDA, geospatial features, clustering, XGBoost model and evaluation
data_preparation.py         # reusable EDA and cleaning functions
```

## Tech

Python · pandas · GeoPandas · scikit-learn · XGBoost · Matplotlib · Seaborn

*Developed as part of my MSc Data Analytics (Data Mining & Machine Learning module).*
