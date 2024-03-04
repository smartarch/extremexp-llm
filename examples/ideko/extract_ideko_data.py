"""
Extracts the data from .zip files into folders. Then extracts features (mean, std) from the data.

Note that the resulting file paths are really long, so on Windows, maximum file path limit might have to be increased (see https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry)
"""
from shutil import unpack_archive
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
import csv
from tqdm import tqdm

EXTRACT_ZIP_FILES = False
EXTRACT_DATA = True

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

ideko_data_folder = Path(__file__).parent / os.environ["IDEKO_DATA_FOLDER"]
new_data_file = Path(__file__).parent / os.environ["NEW_DATA_FILE"]

ideko_data_folder = ideko_data_folder.resolve()
new_data_file = new_data_file.resolve()

if EXTRACT_ZIP_FILES:
    print("Extracting zip files...")

    data_files = list(ideko_data_folder.glob("*/*.zip"))
    print("Number of files:", len(data_files))

    for file in tqdm(data_files):
        print("unpacking", file)
        unpack_archive(file, file.parent / file.stem)

    print("Done extracting zip files")

if EXTRACT_DATA:
    print("Extracting data...")

    def std_mean_positive_negative(df):
        # TODO: do something more clever (e.g. mean and std for each forward and backward movement)
        positive_mean = df[df['f3'] > 0]['f3'].mean()
        negative_mean = df[df['f3'] < 0]['f3'].mean()
        positive_std = df[df['f3'] > 0]['f3'].std()
        negative_std = df[df['f3'] < 0]['f3'].std()
        total_std = df['f3'].std()
        return positive_mean, negative_mean, positive_std, negative_std, total_std
    
    ideko_csv_files = sorted(ideko_data_folder.rglob('*.csv'))
    print("Number of files:", len(ideko_csv_files))

    with open(new_data_file, 'w', newline='') as new_data_csv:
        csv_writer = csv.writer(new_data_csv)
        csv_writer.writerow(['positive_mean', 'negative_mean', 'positive_std', 'negative_std', 'total_std'])

        for csv_file in tqdm(ideko_csv_files):
            df = pd.read_csv(csv_file, delimiter=';')
            csv_writer.writerow(std_mean_positive_negative(df))
    
    print("Done extracting data")
