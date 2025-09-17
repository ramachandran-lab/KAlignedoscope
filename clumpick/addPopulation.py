import pandas as pd
import os
import glob

population_df = pd.read_csv("input_data/1kg_PopulationColumn.csv")

chicken_df = population_df[['Population']]

replicate_folder = "input_data/1kg"

replicate_files = glob.glob(os.path.join(replicate_folder, "*.csv"))

# Loop over each file and append population data
for file_path in replicate_files:
    # Read replicate data
    rep_df = pd.read_csv(file_path)

    # Check that the number of rows match
    if len(rep_df) != len(chicken_df):
        print(f"⚠️ Row count mismatch in {os.path.basename(file_path)} — skipping.")
        continue

    # Concatenate side-by-side
    merged_df = pd.concat([rep_df, chicken_df], axis=1)

    cols = merged_df.columns.tolist()

    # Remove the columns we're going to move
    cols.remove('Population')

    # Rebuild the column order: [first column] + ['Individual', 'Population'] + rest
    new_order = [cols[0], 'Population'] + cols[1:]

    # Apply the new column order
    merged_df = merged_df[new_order]



    # Create output file path
    output_folder="input_data/1kg_pop"
    base_name = os.path.basename(file_path).replace(".csv", "_with_pop.csv")
    output_path = os.path.join(output_folder, base_name)

        # Save the updated file
    merged_df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}")
