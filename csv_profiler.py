import argparse
import pandas as pd
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description="CSV Profiler CLI Tool")
    parser.add_argument("file", help="Path to the CSV file")
    return parser.parse_args()

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except pd.errors.ParserError:
        print("Error: File could not be parsed. Please check the format.")
        exit(1)

def basic_stats(df):
    return {
        "Row Count": len(df),
        "Column Count": len(df.columns),
        "Nulls per Column": df.isnull().sum().to_dict(),
        "Data Types": df.dtypes.astype(str).to_dict()
    }

def numeric_stats(df):
    numeric_df = df.select_dtypes(include="number")
    return numeric_df.describe().T.to_dict()

def categorical_stats(df):
    categorical_df = df.select_dtypes(include="object")
    return categorical_df.nunique().to_dict()

def print_summary(stats, numeric, categorical):
    print("\n--- Basic Stats ---")
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n--- Numeric Columns ---")
    print(tabulate(pd.DataFrame(numeric).T, headers="keys", tablefmt="grid"))

    print("\n--- Categorical Columns (Unique Value Count) ---")
    print(tabulate(categorical.items(), headers=["Column", "Unique Values"], tablefmt="grid"))

def main():
    args = parse_args()
    df = load_csv(args.file)
    stats = basic_stats(df)
    numeric = numeric_stats(df)
    categorical = categorical_stats(df)
    print_summary(stats, numeric, categorical)

if __name__ == "__main__":
    main()
