import argparse
import os
import re
from collections import defaultdict
import pandas as pd
import numpy as np

from .funcs import load_files, load_pong_acrossK
from .html import generate_html_content

def main(args):


    print("Membership matrix files:",args.processed_membership)
    print("Input tool:", args.input_tool)
    print("Alignment file:", args.alignment_file)
    print("Alignment per-K file:", args.alignment_perK_file)
    print("Alignment across-K file:", args.alignment_acrossK_file)

    if args.alignment_file is not None:
        assert os.path.isfile(args.alignment_file), f"Alignment file not found: {args.alignment_file}"
        assert args.input_tool == "clumppling", "Alignment file is only applicable for Clumppling input."
    if args.alignment_perK_file is not None:
        assert os.path.isfile(args.alignment_perK_file), f"Alignment file not found: {args.alignment_perK_file}"
        assert args.input_tool == "pong", "Alignment per-K file is only applicable for Pong input."
    if args.alignment_acrossK_file is not None:
        assert os.path.isfile(args.alignment_perK_file), f"Alignment file not found: {args.alignment_acrossK_file}"
        assert args.input_tool == "pong", "Alignment across-K file is only applicable for Pong input."

    input_folder = args.input
    output_folder = args.processed_membership
    label_file = args.label_file
    os.makedirs(output_folder, exist_ok=True)

    if args.label_file:
        labels = np.loadtxt(args.label_file, delimiter=",", dtype=str, skiprows=0)

    if args.input_tool == "pong":
        major_mode_names = load_pong_acrossK(args.alignment_acrossK_file)
        # print("Major mode names extracted from PONG alignment file:", major_mode_names)

        # pat = re.compile(r'^(k(?P<k>\d+)r(?P<r>\d+))_reprun\.Q$', re.IGNORECASE)
        # by_k = defaultdict(list)

        # for filename in os.listdir(input_folder):
        #     if not filename.endswith(".Q"):
        #         continue
        #     m = pat.match(filename)
        #     if not m:
        #         continue

        #     suffix = m.group(1).lower()        # 'k2r7'
        #     k_val = int(m.group('k'))          # 2
        #     by_k[k_val].append(suffix)

        # # optional: de-dupe and sort each list by R value numerically
        # for k, lst in by_k.items():
        #     # unique while preserving lowest R first
        #     rnum = lambda s: int(re.search(r'r(\d+)', s).group(1))
        #     lst[:] = sorted(dict.fromkeys(lst), key=rnum)

        # mbsp_files = dict(by_k)
        # print(mbsp_files)

        # for major_mode_name in major_mode_names:
        #     print(f"Processing major mode: {major_mode_name}")
        #     k_val = int(major_mode_name.split('r')[0].strip('k'))  # Extract K value from 'KxrY'
        #     print(k_val)
        #     orig_list = mbsp_files.get(k_val, [])
        #     print(orig_list)
        #     if not orig_list:
        #         print(f"  No files found for K={k_val}, skipping.")
        #         continue
        #     for i, suffix in enumerate(orig_list):
        #          if suffix == major_mode_name:
        #             orig_list.insert(0, orig_list.pop(i))
        #             break
        #     print(f"  Reordered files for K={k_val}: {orig_list}")
        #     for i, suffix in enumerate(orig_list):
        #         input_path = os.path.join(input_folder, f"{suffix}_reprun.Q")
        #         output_filename = f"K{k_val}M{i+1}.csv"
        #         output_path = os.path.join(output_folder, output_filename)

        #         # Load the .Q file (whitespace-delimited, no header)
        #         df = pd.read_csv(input_path, delim_whitespace=True, header=None)

        #         # Add individual names and move to first column
        #         df["name"] = [f"Ind{i+1}" for i in range(len(df))] 
        #         df = df[["name"] + [c for c in df.columns if c != "name"]]

        #         # Rename numeric columns to Cluster1..ClusterN
        #         num_clusters = df.shape[1] - 1
        #         df.columns = ["name"] + [f"Cluster{i+1}" for i in range(num_clusters)]

        #         if args.label_file:
        #             # Add labels as second column
        #             df["Population"] = labels
        #             df = df[["name", "Population"] + [c for c in df.columns if c not in ["name", "Population"]]]
        #             print(f"populations added from {args.label_file}")


        #         # Save
        #         df.to_csv(output_path, index=False)
        #         print(f"✅ Saved: {output_filename}")
        
        # dummy_path = os.path.join(os.getcwd(), "dummy_alignment.txt")
        # print("Creating dummy alignment file at:", dummy_path)
        # with open(dummy_path, "w") as f:
        #     f.write("")  # just an empty file
        # args.alignment_file = dummy_path
       
    else:
        # Robust detectors (case-insensitive, allow separators/spaces)
        K_RE = re.compile(r'[kK]\s*_?\s*(\d+)')
        M_RE = re.compile(r'[mM]\s*_?\s*(\d+)')

        #print(f"Processing .Q files from: {input_folder}")
    
        for filename in os.listdir(input_folder):
            if not filename.endswith(".Q"):
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
            if m_match:
                m_num = m_match.group(1)
            else:
                # Look for reprun and capture the number after 'r'
                reprun_match = re.search(r"reprun(\d+)", filename, re.IGNORECASE)
                if reprun_match:
                    m_num = reprun_match.group(1)
                else:
                    m_num = "1"  # default fallback

            # m_num = m_match.group(1) if m_match else "1"   # default M -> 1

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
                print(f"populations added from {args.label_file}")


            # Save
            df.to_csv(output_path, index=False)
            #print(f"✅ Saved: {output_filename}")

        
        data_json, alignment_json = load_files(args.processed_membership, args.alignment_file)

        # MAIN    
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
    parser.add_argument('--alignment_file', type=str, required=False, help='Input file containing the cluster alignment (from Clumppling).')
    parser.add_argument('--alignment_perK_file', type=str, required=False, help='Input file containing the cluster alignment per-K (from Pong).')
    parser.add_argument('--alignment_acrossK_file', type=str, required=False, help='Input file containing the cluster alignment across-K (from Pong).')
    parser.add_argument('--input_tool', type=str, choices=['clumppling', 'pong'], default='clumppling', help='Tool that generated the input files.')

    args = parser.parse_args()


    main(args)