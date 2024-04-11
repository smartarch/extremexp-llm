"""Computes the mean and standard deviation of values from the 'score' column across several CSV files. Partially written by ChatGPT."""

from pathlib import Path
import pandas as pd
import numpy as np
import sys

def compute_statistics(files):
    # Load the CSV files and extract the 'score' column
    scores = []
    patterns = None
    categories = None
    for idx, file in enumerate(files):
        df = pd.read_csv(file)
        if 'score' in df.columns:
            scores.append(df['score'])

            # For the first file, also store the pattern and category values
            if idx == 0:
                if 'pattern' in df.columns:
                    patterns = df[['pattern']]
                if 'category' in df.columns:
                    categories = df[['category']]
        else:
            raise ValueError(f"'score' column not found in {file}")
    
    # Ensure all CSVs have the same number of rows
    row_counts = [len(score) for score in scores]
    if len(set(row_counts)) > 1:
        raise ValueError("CSV files have different number of rows.")
    
    # Compute mean and standard deviation row-wise
    results = []
    for i in range(row_counts[0]):
        row_scores = [score[i] for score in scores]
        mean = np.mean(row_scores)
        std_dev = np.std(row_scores)
        results.append([mean, std_dev])
    
    # Convert results to a DataFrame and save or print
    result_df = pd.DataFrame(results, columns=['Mean', 'Standard Deviation'])

    # Add the 'pattern' and 'category' columns from the first file
    if patterns is not None:
        result_df = pd.concat([patterns.reset_index(drop=True), result_df], axis=1)
    if categories is not None:
        result_df = pd.concat([categories.reset_index(drop=True), result_df], axis=1)

    print(result_df)
    # To save to a CSV file, uncomment the next line and specify your filename
    # result_df.to_csv('output.csv', index=False)

    print()
    for _, row in result_df.iterrows():
        print(f"${row['Mean']:.2f}\\pm{row['Standard Deviation']:.2f}$")

if __name__ == "__main__":

    files = []
    # glob = "3/*.patterns.csv"
    glob = "3/*.categories.csv"
    files = list((Path(__file__).parent.parent / "agent_evaluation_logs").glob(glob))

    # Expects file paths to CSV files as command-line arguments
    if files == []:
        files = sys.argv[1:]
    if len(files) < 1:
        print("Usage: python script.py file1.csv file2.csv ...")
    else:
        print([str(f) for f in files])
        compute_statistics(files)
