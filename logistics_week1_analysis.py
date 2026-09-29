"""
Logistics Data Analyst Internship - Week 1
Illustrative analysis script.

Expected columns in the CSV:
dispatch_date, delivery_date, promised_date
Other optional columns can include distance, transport_cost,
vehicle_type, shipping_mode, quantity, weight, traffic_condition, weather.
"""

import pandas as pd

FILE = "logistics_data.csv"

df = pd.read_csv(FILE)

print("Shape:", df.shape)
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

# Date conversion
date_cols = ["dispatch_date", "delivery_date", "promised_date"]
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Feature engineering
if {"dispatch_date", "delivery_date"}.issubset(df.columns):
    df["delivery_days"] = (df["delivery_date"] - df["dispatch_date"]).dt.total_seconds() / 86400

if {"delivery_date", "promised_date"}.issubset(df.columns):
    df["delay_days"] = (df["delivery_date"] - df["promised_date"]).dt.total_seconds() / 86400
    df["delay_flag"] = (df["delay_days"] > 0).astype(int)

# KPIs
if "delay_flag" in df.columns:
    on_time_rate = (1 - df["delay_flag"].mean()) * 100
    print(f"\nOn-Time Delivery Rate: {on_time_rate:.2f}%")

if "delivery_days" in df.columns:
    print(f"Average Delivery Time: {df['delivery_days'].mean():.2f} days")

if "delay_days" in df.columns:
    delayed = df.loc[df["delay_flag"] == 1, "delay_days"]
    if len(delayed):
        print(f"Average Delay Among Late Orders: {delayed.mean():.2f} days")

if "transport_cost" in df.columns:
    print(f"Average Transport Cost: {df['transport_cost'].mean():.2f}")

# Grouped KPI example
if "shipping_mode" in df.columns and "delay_flag" in df.columns:
    mode_summary = (
        df.groupby("shipping_mode")
          .agg(
              orders=("delay_flag", "size"),
              on_time_rate=("delay_flag", lambda x: (1-x.mean())*100),
          )
          .reset_index()
    )
    print("\nPerformance by Shipping Mode:")
    print(mode_summary.sort_values("on_time_rate", ascending=False))

# Numeric correlation
numeric = df.select_dtypes(include="number")
if "delivery_days" in numeric.columns:
    print("\nCorrelation with delivery_days:")
    print(numeric.corr()["delivery_days"].sort_values())

print("\nAnalysis completed.")
