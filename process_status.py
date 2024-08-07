import pandas as pd


def process_status(folder_path):
    path1 = folder_path.joinpath('merged').joinpath('vms_table.csv')
    path2 = folder_path.joinpath('merged').joinpath('job_final.csv')
    path3 = folder_path.joinpath('do not post').joinpath('do-not-post-simplify.csv')
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
    
    # Check if DataFrames are not empty
    if not df1.empty and not df2.empty:
        # Merge the DataFrames
        df1 = df1[df1['Status'] == 'Open']
        merged_df = pd.merge(df1, df2, left_on='Job ID', right_on='External Job Posting Id', how='outer')
        
        merged_df = merged_df[['Job ID', 'Status' ,'Job Status']]
        
        filter_df = merged_df
        
        merged_df['result'] = merged_df['Status'] == merged_df['Job Status']
        merged_df = merged_df.dropna(subset=['Job ID'])
        merged_df = merged_df[merged_df['result'] == False]
        merged_df = merged_df.dropna(subset=['Job Status'])
        merged_df = merged_df.dropna(subset=['Status'])
        merged_df = merged_df.sort_values(by='Job Status',ascending=True)
        merged_df['Job ID'] = merged_df['Job ID'].astype('Int64')
        
        
        # Specify the path to save the merged CSV file
        output_file_path = folder_path.joinpath('result', 'Status.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the merged DataFrame to a new CSV file
        merged_df.to_csv(output_file_path, index=False)
        
                
        # Filter the DataFrame for 'Job Status' isna
        filtered_df = filter_df[filter_df['Job Status'].isna()]

        # Cast 'Job ID' to 'Int64' and dropna
        job_ids = filtered_df['Job ID'].astype('Int64').dropna()

        # Extract remaining IDs
        remaining_ids = set(job_ids)
        dnt_ids = set(df3['JOBID'].dropna())

        # Find the difference between sets
        remaining_ids = remaining_ids - dnt_ids

        # Convert the set to a DataFrame
        remaining_ids_df = pd.DataFrame(list(remaining_ids), columns=['RemainingJobIds'])

        # Create output file path and directory
        output_file_path = folder_path.joinpath('result', 'Posting.csv')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the DataFrame to a new CSV file
        remaining_ids_df.to_csv(output_file_path, index=False)

        print(f"Processing done. Output saved to: {output_file_path}")
    else:
        print("One or both of the input CSV files are empty.")
        
        

