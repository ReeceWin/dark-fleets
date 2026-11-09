"""
This script performs exploratory data analysis and data preparation on the AIS disabling events dataset.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


def load_data():
    df = pd.read_csv("ais_disabling_events.csv")
    gdf = gpd.read_file("eez_v12_lowres.shp")
    return df, gdf

def exploratory_data_analysis(df, gdf):
    """
    Perform exploratory data analysis on the dataframe.
    """
    print("===========HEAD===========")
    print(df.head(20))
    print("===========INFO===========")
    print(df.info())
    print("===========DESCRIBE===========")
    print(df.describe())
    print("===========ISNULL===========")
    print(df.isnull().sum())
    print("===========NUNIQUE===========")
    print(df.nunique())
    print("===========VALUE COUNTS===========")
    print(df["flag"].value_counts())
    
def data_preparation(df):
    """
    Fill null values in the 'flag' column with 'Unknown' with the assumption
    that the flag is unknown if it is not recorded.
    """
    df["flag"] = df["flag"].fillna("Unknown")
    df.dropna(subset=["flag"], inplace=True)
    df.to_csv("ais_disabling_events_cleaned.csv", index=False)
    return df

def calculate_distance(ais_gdf, ais_end_gdf):
    """
    Calculate the distance between the start and end points of the disabling events.
    """
    distance = ais_gdf.distance(ais_end_gdf)
    return distance

def calculate_distance_from_shore_shift(df):
    """
    Calculate the distance from the shore shift of the disabling events.
    """
    df["distance_from_shore_shift"] = df["gap_start_distance_from_shore_m"] - df["gap_end_distance_from_shore_m"]
    return df

def generate_histogram_of_gap_hours(df):
    """
    Generate a histogram of the gap hours of the disabling events.
    """
    df["gap_hours"] = df["gap_hours"].astype(float)
    df["gap_hours"].hist(bins=50)
    plt.title("Histogram of Gap Hours")
    plt.xlabel("Gap Hours")
    plt.ylabel("Frequency")
    plt.show()

def generate_statistics_of_gap_hours(df):
    """
    Generate statistics of the gap hours of the disabling events.
    """
    print("===========GAP HOURS STATISTICS===========")
    print(df["gap_hours"].describe())
    print("90th PERCENTILE OF GAP HOURS")
    print(df["gap_hours"].quantile(0.9))
    print("95th PERCENTILE OF GAP HOURS")
    print(df["gap_hours"].quantile(0.95))
    print("99th PERCENTILE OF GAP HOURS")
    print(df["gap_hours"].quantile(0.99))

def plot_correlation_heatmap(df):
    """
    Generate a heatmap to identify relationships between numerical features.
    """
    # Select only numerical columns for correlation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calculate the correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Create the plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap of AIS Event Features")
    plt.show()

def main():
    df, gdf = load_data()
    print(df.columns)
    print(f"EEZ CRS: {gdf.crs}")
    print(f"EEZ HEAD: {gdf.head()}")
    gdf.to_csv("eez_v12_lowres.csv", index=False)
    gdf_crs = gdf.crs
    # Converting the AIS df Long and Lat into a "point" object
    ais_gdf = gpd.GeoDataFrame(
        df, # AIS DF
        geometry=gpd.points_from_xy(df['gap_start_lon'], df['gap_start_lat']), # Creating a geometry column converting Lon Lat to Point
        crs="EPSG:4326" # Using the standard GPS system
    )

    ais_end_gdf = gpd.GeoDataFrame(
        df, # AIS DF
        geometry=gpd.points_from_xy(df['gap_end_lon'], df['gap_end_lat']), # Creating a geometry column converting Lon Lat to Point
        crs="EPSG:4326" # Using the standard GPS system
    )
    print("===============AIS GDF===============")
    print(ais_gdf.head())
    print("===============AIS END GDF===============")
    print(ais_end_gdf.head())
    print("==========================================")
    ais_gdf = ais_gdf.to_crs(gdf_crs)
    ais_end_gdf = ais_end_gdf.to_crs(gdf_crs)
    df["distance_meters"] = calculate_distance(ais_gdf, ais_end_gdf)
    df["distance_nm"] = df["distance_meters"] / 1852
    df = calculate_distance_from_shore_shift(df)
    print(df.head())
    generate_histogram_of_gap_hours(df)
    plot_correlation_heatmap(df)
    generate_statistics_of_gap_hours(df)
    """
    print(df.shape)
    exploratory_data_analysis(df, ais_gdf)
    df = data_preparation(df)
    print(df.isnull().sum())
    print(df.shape)
    """

if __name__ == "__main__":
    main()

    
    