import pandas as pd


def process_closing(folder_path):
    path1 = folder_path.joinpath('merged').joinpath('vms_table.csv')
    path2 = folder_path.joinpath('merged').joinpath('job_final.csv')
    path3 = folder_path.joinpath('do not post').joinpath('do-not-closing-simplify.csv')
    print(f"Processing VMS: {path1}")
    print(f"Processing Job Board files from: {path2}")
    print(f"Processing DNP: {path3}")

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

    try:
        df3 = pd.read_csv(path3)
    except FileNotFoundError:
        print(f"File not found: {path3}")
        return
    
    if not df1.empty and not df2.empty:
        # Merge the DataFrames
        df1 = df1[df1['Status'] == 'Filled']
        merged_df = pd.merge(df2, df1, left_on='External Job Posting Id', right_on='Job ID', how='right')
        
        merged_df = merged_df[['Job ID', 'External Job Posting Id']]
        merged_df = merged_df.dropna(subset=['External Job Posting Id'])
        merged_df['External Job Posting Id'] = merged_df['External Job Posting Id'].astype('Int64')
        
        job_ids = merged_df['Job ID'].astype('Int64').dropna()

        # Extract remaining IDs
        remaining_ids = set(job_ids)
        dnt_ids = set(df3['Job Id'].dropna())

        # Find the difference between sets
        remaining_ids = remaining_ids - dnt_ids

        # Convert the set to a DataFrame
        remaining_ids_df = pd.DataFrame(list(remaining_ids), columns=['Closing'])
        
    
     # Specify the path to save the merged CSV file
    output_file_path = folder_path.joinpath('result', 'Closing.csv')
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the merged DataFrame to a new CSV file
    remaining_ids_df.to_csv(output_file_path, index=False)