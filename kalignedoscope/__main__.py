import argparse
import os
import re
import pandas as pd
import numpy as np

from .funcs import load_files
from .html import generate_html_content

def main(args):


    print(args.processed_membership)
    print(args.alignment_file)

    input_folder = args.input
    output_folder = args.processed_membership
    label_file = args.label_file
    os.makedirs(output_folder, exist_ok=True)

    # Robust detectors (case-insensitive, allow separators/spaces)
    K_RE = re.compile(r'[kK]\s*_?\s*(\d+)')
    M_RE = re.compile(r'[mM]\s*_?\s*(\d+)')

    if args.label_file:
        labels = np.loadtxt(args.label_file, delimiter=",", dtype=str, skiprows=0)

    for filename in os.listdir(input_folder):
        if filename.endswith(".Q"):
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
        output_filename = f"K{k_num}M{m_num}.csv"
        output_path = os.path.join(output_folder, output_filename)

        # Load the .Q file (whitespace-delimited, no header)
        df = pd.read_csv(input_path, delim_whitespace=True, header=None)

        # Add individual names and move to first column
        df["name"] = [f"Ind{i+1}" for i in range(len(df))] 
        df = df[["name"] + [c for c in df.columns if c != "name"]]

        # Rename numeric columns to Cluster1..ClusterN
        num_clusters = df.shape[1] - 1
        df.columns = ["name"] + [f"Cluster{i+1}" for i in range(num_clusters)]

        if args.label_file:
            # Add labels as second column
            df["Population"] = labels
            df = df[["name", "Population"] + [c for c in df.columns if c not in ["name", "Population"]]]

        # Save
        df.to_csv(output_path, index=False)
        print(f"✅ Saved: {output_filename}")

    # MAIN
    data_json, alignment_json = load_files(args.processed_membership, args.alignment_file)
    html_content = generate_html_content(data_json, alignment_json)
    


# def parse_args():
#     #parser.add_argument('--output', type=str, required=True, help='Output file to save results.')
#     #parser.add_argument('--method', type=str, choices=['kmeans', 'hierarchical'], default='kmeans', help='Clustering method to use.')
#     return parser.parse_args()



# Now i want to generate html content

if __name__ =="__main__":

    parser = argparse.ArgumentParser(description="KAlignedoscope: A tool for clustering and mapping genomic data.")
        
    parser.add_argument("--input", "-i", type=str, help="Input folder with .Q files")
    parser.add_argument("--label_file",  type=str, help="Optional file with individual labels to add as the second column", default=None)
    parser.add_argument('--processed_membership', type=str, required=True, help='Input folder containing the clustering result files.')
    parser.add_argument('--alignment_file', type=str, required=True, help='Input file containing the cluster alignment.')
    

    args = parser.parse_args()

    main(args)