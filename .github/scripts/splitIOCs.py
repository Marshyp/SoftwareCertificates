## Python Script developed by https://marshsecurity.org/ to allow for the splitting of a bulk CSV into 500-row batches.
## Currently, MDE import only allows a maximum of 500 rows on each import.

import pandas as pd
import os
import glob

# Input and output directories from environment variables
input_dir = os.getenv('INPUT_DIR', 'Bulk-IOC-CSVs')
output_dir = os.getenv('OUTPUT_DIR', 'Bulk-IOC-CSVs/for_review')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the maximum number of rows per batch (including header row)
max_rows_per_batch = 500

# Process each CSV file in the input directory
for file_path in glob.glob(f'{input_dir}/*.csv'):
    print(f"Processing file: {file_path}")

    # Load the CSV file
    df = pd.read_csv(file_path)

    # Split the dataframe into batches
    batches = []
    for start_row in range(1, df.shape[0], max_rows_per_batch - 1):  # 499 data rows + 1 header
        batch = df.iloc[start_row:start_row + max_rows_per_batch - 2]
        batch_with_header = pd.concat([df.iloc[:1], batch], ignore_index=True)
        batches.append(batch_with_header)

    # Save each batch to a separate CSV file
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    for i, batch in enumerate(batches, start=1):
        batch_file_path = os.path.join(output_dir, f'{base_filename}_batch_{i}.csv')
        batch.to_csv(batch_file_path, index=False)

    print(f"Batches for {file_path} saved to {output_dir}")
