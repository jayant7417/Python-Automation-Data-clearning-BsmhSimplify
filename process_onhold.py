import pandas as pd


def process_onhold(folder_path):
    path1 = folder_path.joinpath('merged').joinpath('vms_table.csv')
    path2 = folder_path.joinpath('merged').joinpath('job_final.csv')
    print(f"Processing VMS: {path1}")
    print(f"Processing Job Board files from: {path2}")
    

    # Read the CSV files into DataFrames
    try:
        df1 = pd.read_csv(path1)
    except FileNotFoundError:
        print(f"File not found: {path1}")
        return

    try:
        df2 = pd.read_csv(path2)
    except FileNotFoundError:
        print(f"File not found: {path2}")
        return
    
    # Check if DataFrames are not empty
    if not df1.empty and not df2.empty:
        df2 = df2[df2['Job Status'] == 'On-Hold']
        merged_df = pd.merge(df2, df1, left_on='External Job Posting Id', right_on='Job ID', how='outer')

        merged_df = merged_df[['External Job Posting Id','Job ID']]

        merged_df = merged_df.dropna(subset=['External Job Posting Id'])
        
        merged_df = merged_df[merged_df['Job ID'].isna()]
        
        merged_df = merged_df[['External Job Posting Id']]

        # Correct way to convert 'External Job Posting Id' column to Int64
        merged_df['External Job Posting Id'] = merged_df['External Job Posting Id'].astype('Int64')


     # Create output file path and directory
        output_file_path = folder_path.joinpath('result', 'On-Hold.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the DataFrame to a new CSV file
        merged_df.to_csv(output_file_path, index=False)

        print(f"Processing done. Output saved to: {output_file_path}")
    else:
        print("One or both of the input CSV files are empty.")

