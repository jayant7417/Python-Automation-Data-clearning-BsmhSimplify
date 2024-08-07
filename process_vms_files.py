import os
import pandas as pd


def process_vms_files(folder_path):
    dfs = []
    path = folder_path.joinpath('merged')
    print(f"Processing VMS files from: {path}")

    for filename in os.listdir(path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(path, filename)
            df = pd.read_excel(file_path, skiprows=4, engine='openpyxl')  # Skip the first 4 rows
            df['Source_File'] = filename
            dfs.append(df)

    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        # Adjust column selection based on identified headers
        relevant_columns = ['Job ID', 'Status']  # Change based on actual headers
        merged_df = merged_df[relevant_columns]
        
        """merged_df['Status'] =  merged_df['Status'].replace('Sourcing','Open')
        merged_df['Status'] =  merged_df['Status'].replace('Re-open','Open')"""
        
        replace_patterns = ['Sourcing', 'Re-open']
        for pattern in replace_patterns:
            merged_df['Status'] = merged_df['Status'].str.replace(pattern, 'Open', regex=False)

        output_file_path = folder_path.joinpath('merged', 'vms_table.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        merged_df.to_csv(output_file_path, index=False)
        print("done")