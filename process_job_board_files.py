import os

import pandas as pd


def process_job_board_files(folder_path):
    dfs = []
    path = folder_path.joinpath('job board')
    print(f"Processing Job Board files from: {path}")
    
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            file_path = os.path.join(path, filename)
            df = pd.read_csv(file_path)
            df['Source_File'] = filename
            dfs.append(df)
    
    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df.drop_duplicates(subset='External Job Posting Id', inplace=True)
        merged_df = merged_df[['External Job Posting Id', 'Job Status']]
        
        # Convert to numeric, coerce errors to NaN
        merged_df['External Job Posting Id'] = pd.to_numeric(merged_df['External Job Posting Id'], errors='coerce')

        merged_df = merged_df.dropna()
        
        # Fill NaN values with a placeholder
        #merged_df['External Job Posting Id'].fillna(0, inplace=True)

        # Convert the column to integers
        merged_df['External Job Posting Id'] = merged_df['External Job Posting Id'].astype(int)

        
        
        output_file_path = folder_path.joinpath('merged', 'job_final.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        merged_df.to_csv(output_file_path, index=False)
        print(f"Job Board processing done. Output saved to: {output_file_path}")
    else:
        print("No Job Board CSV files found or processed.")