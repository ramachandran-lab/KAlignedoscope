import os
import re
import pandas as pd

# -------- settings --------
input_folder  = r"C:/Users/13172/Downloads/my_d3_visualization/input_data/modes_aligned_1k"
output_folder = r"C:/Users/13172/Downloads/my_d3_visualization/input_data/1kg"
dataset_prefix = "processed"  # change if needed
os.makedirs(output_folder, exist_ok=True)

# Robust detectors (case-insensitive, allow separators/spaces)
K_RE = re.compile(r'[kK]\s*_?\s*(\d+)')
M_RE = re.compile(r'[mM]\s*_?\s*(\d+)')

for filename in os.listdir(input_folder):
    if not filename.endswith(".Q") or filename == "all_modes_alignment_avg.txt":
        continue

    input_path = os.path.join(input_folder, filename)

    # Try to find K and M anywhere in the filename (before extension)
    stem = os.path.splitext(filename)[0]

    k_match = K_RE.search(stem)
    m_match = M_RE.search(stem)

    if not k_match:
        # If there's truly no K in the name, you can choose to skip or set a default.
        # Here we skip, since downstream grouping relies on K existing.
        print(f"⚠️ Skipping (no K found): {filename}")
        continue

    k_num = k_match.group(1)
    m_num = m_match.group(1) if m_match else "1"   # default M -> 1

    # Unified output name (no underscore between K… and M… to match your original regex)
    # Example: capeverde_K11111M2.csv
    output_filename = f"{dataset_prefix}_K{k_num}M{m_num}.csv"
    output_path = os.path.join(output_folder, output_filename)

    # Load the .Q file (whitespace-delimited, no header)
    df = pd.read_csv(input_path, delim_whitespace=True, header=None)

    # Add individual names and move to first column
    df["name"] = [f"Ind{i+1}" for i in range(len(df))] 
    df = df[["name"] + [c for c in df.columns if c != "name"]]

    # Rename numeric columns to Cluster1..ClusterN
    num_clusters = df.shape[1] - 1
    df.columns = ["name"] + [f"Cluster{i+1}" for i in range(num_clusters)]

    # Save
    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_filename}")
