import pandas as pd
import os
def process_pickled_files(file_paths):
    data_records = []

    for filepath in file_paths:
        if filepath.endswith('.pkl'):
            df = pd.read_pickle(filepath)
            
            # Identify columns that start with 'CODES_DEFAUT'
            default_code_columns = [col for col in df.columns if col.startswith('CODES_DEFAUT')]
            print("Columns identified:", default_code_columns)
            
            if default_code_columns:
                # Collect unique values for each code column
                for column in default_code_columns:
                    unique_values = df[column].dropna().unique()
                    sorted_values = sorted(map(str, unique_values))  # Sort values in ascending order
                    num_unique_values = len(sorted_values)
                    
                    data_records.append({
                        'Filename': os.path.basename(filepath),
                        'Default_Code': column,
                        'Num_Distinct_Values': num_unique_values
                    })
                    
                    # Append sorted distinct values as separate records
                    for i, value in enumerate(sorted_values):
                        data_records.append({
                            'Filename': os.path.basename(filepath),
                            'Default_Code': column,
                            'Value_Index': i + 1,
                            'Code_Value': value
                        })

    if data_records:
        # Create a DataFrame from the collected records
        temp_df = pd.DataFrame(data_records)
        
        # Separate distinct value columns
        value_df = temp_df[temp_df['Value_Index'].notna()].pivot_table(
            index=['Filename', 'Default_Code'],
            columns='Value_Index',
            values='Code_Value',
            aggfunc='first'
        ).reset_index()

        # Add number of distinct values to the DataFrame
        count_df = temp_df[temp_df['Value_Index'].isna()].drop(columns='Value_Index')
        
        # Merge the count and value DataFrames
        final_df = pd.merge(count_df, value_df, on=['Filename', 'Default_Code'], how='left')

        # Generate column names dynamically
        num_values = len(final_df.columns) - 3  # Exclude Filename, Default_Code, and Num_Distinct_Values
        new_column_names = ['Filename', 'Default_Code', 'Num_Distinct_Values'] + \
            [f'Value_{i}' for i in range(num_values)]

        # Ensure the number of new column names matches the number of columns in final_df
        if len(new_column_names) != len(final_df.columns):
            raise ValueError(f"Length mismatch: Expected axis has {len(final_df.columns)} elements, new values have {len(new_column_names)} elements")

        final_df.columns = new_column_names

        output_filepath = os.path.join(os.path.dirname(file_paths[0]), 'Report.pkl')
        final_df = final_df.drop('Value_0', axis=1, errors='ignore')  # Use errors='ignore' to avoid KeyError if 'Value_0' is not present
        final_df.to_pickle(output_filepath)  # Removed index=False as it's not supported for to_pickle
    else:
        print("No pickled files with 'DEFAULT_CODE' columns were found.")