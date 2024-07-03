"""Computes the mean and standard deviation of values from the 'score' column across several CSV files. Partially written by ChatGPT."""

from pathlib import Path
import pandas as pd
import numpy as np
import sys

AGG_COLUMN = "pattern"
# AGG_COLUMN = "category"
VARIANT = 2

def compute_statistics(files):
    # Combine all scores into one DataFrame with associated patterns
    data_frames = []
    for file in files:
        df = pd.read_csv(file)
        if 'score' in df.columns and AGG_COLUMN in df.columns:
            data_frames.append(df[[AGG_COLUMN, 'score']])
        else:
            raise ValueError(f"'score' or '{AGG_COLUMN}' column not found in {file}")
    
    # Concatenate all data frames
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    # Group by 'pattern' and calculate mean and standard deviation
    result_df = combined_df.groupby(AGG_COLUMN, sort=False)['score'].agg(['mean', 'std', 'size']).reset_index()
    result_df.columns = [AGG_COLUMN, 'Mean', 'Standard Deviation', 'Repetitions']
    
    print(result_df)
    # To save to a CSV file, uncomment the next line and specify your filename
    # result_df.to_csv('output.csv', index=False)

    print()
    for _, row in result_df.iterrows():
        print(f"${row['Mean']:.2f}\\pm{row['Standard Deviation']:.2f}$")

if __name__ == "__main__":

    files = []
    if AGG_COLUMN == "pattern":
        glob = f"{VARIANT}/*.patterns.csv"
    else:
        glob = f"{VARIANT}/*.categories.csv"
    files = sorted((Path(__file__).parent.parent / "agent_evaluation_logs" / "gpt_4o").glob(glob))

    # Expects file paths to CSV files as command-line arguments
    if files == []:
        files = sys.argv[1:]
    if len(files) < 1:
        print("Usage: python script.py file1.csv file2.csv ...")
    else:
        print([str(f) for f in files])
        compute_statistics(files)
