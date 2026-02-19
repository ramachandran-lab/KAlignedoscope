import argparse
import os
import re
import pandas as pd
import numpy as np

from .funcs import load_files, load_pong_acrossK
from .html import generate_html_content


# Order of operations!
# sanity checks and validations
# check if required input files exist (if not, raise FileNotFoundError)
# check if intermediate file already exist (if yes, prompt the user with a warning)
# after initial checks, print the input parameters for confirmation



def _require_dir(path: str, flag: str) -> None:
    if path is None or str(path).strip() == "":
        raise FileNotFoundError(f"Missing required folder for {flag}.")
    if not os.path.isdir(path):
        raise FileNotFoundError(
            f"You may have misspecified the {flag} folder path.\n"
            f"Given: {path}\n"
            "Please double check that this folder exists."
        )


def _require_file(path: str, flag: str) -> None:
    if path is None or str(path).strip() == "":
        raise FileNotFoundError(f"Missing required file for {flag}.")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"You may have misspecified the {flag} path.\n"
            f"Given: {path}\n"
            "Please double check that this file exists."
        )


def _optional_file(path: str | None, flag: str) -> None:
    if path is not None and not os.path.isfile(path):
        raise FileNotFoundError(
            f"You may have misspecified the {flag} path.\n"
            f"Given: {path}\n"
            "Please double check that this file exists."
        )


def _confirm_overwrite_folder(folder: str, what: str = "output folder") -> None:
    """
    If folder exists and is non-empty, prompt user to continue.
    Default is NO unless user types y/yes.
    """
    if os.path.isdir(folder):
        try:
            nonempty = any(True for _ in os.scandir(folder))
        except FileNotFoundError:
            nonempty = False

        if nonempty:
            resp = input(
                f"\n Warning: {what} already exists and contains files:\n"
                f"    {folder}\n"
                "Running may overwrite intermediate files.\n"
                "Continue? [y/N]: "
            ).strip().lower()
            if resp not in {"y", "yes"}:
                raise SystemExit("Aborted by user.")


# Make the validation function here that will run everything

def validate_args(args) -> None:
    # do the existence checks
    _require_dir(args.input, "--input")

    if args.processed_membership is None or str(args.processed_membership).strip() == "":
        raise FileNotFoundError("Missing required folder for --processed_membership.")

    # Optional files must exist if provided
    _optional_file(args.label_file, "--label_file")
    _optional_file(args.mode_stats, "--mode_stats")
    _optional_file(args.alignment_file, "--alignment_file")
    _optional_file(args.alignment_perK_file, "--alignment_perK_file")
    _optional_file(args.alignment_acrossK_file, "--alignment_acrossK_file")

    # provide the intermediate output overwrite warning
    # processed_membership is our intermediate folder 
    _confirm_overwrite_folder(args.processed_membership, what="--processed_membership folder")

    # Check those paths that can exist but still be wrong
    if args.alignment_file is not None and args.input_tool != "clumppling":
        raise ValueError("--alignment_file can only be used with --input_tool clumppling.")

    if (args.alignment_perK_file is not None or args.alignment_acrossK_file is not None) and args.input_tool != "pong":
        raise ValueError("--alignment_perK_file / --alignment_acrossK_file can only be used with --input_tool pong.")

    #remember our value error here if user specifies pong

    if args.input_tool == "pong" and args.alignment_acrossK_file is None:
        raise ValueError("When --input_tool is pong, you must provide --alignment_acrossK_file.")

 

def print_inputs(args) -> None:
    print("\nINPUT PARAMETERS:")
    print("Input tool:", args.input_tool)
    print("Input folder:", args.input)
    print("Processed membership folder:", args.processed_membership)
    print("Label file:", args.label_file)
    print("Alignment file:", args.alignment_file)
    print("Alignment per-K file:", args.alignment_perK_file)
    print("Alignment across-K file:", args.alignment_acrossK_file)
    print("Mode stats:", args.mode_stats)
    print("\n")


# Now we can make the main function that will run the whole thing
# MAIN PIPELINE HERE!

def main(args):
    # first run the sanity checks + validations FIRST
    validate_args(args)

    # ensure processed_membership exists (create after validations + overwrite prompt)
    os.makedirs(args.processed_membership, exist_ok=True)

    # after initial checks, we can  print inputs for confirmation
    print_inputs(args)

    input_folder = args.input
    output_folder = args.processed_membership

    labels = None
    if args.label_file:
        labels = np.loadtxt(args.label_file, delimiter=",", dtype=str, skiprows=0)

    # We will process the .Q files into CSVs here if needed
    if args.input_tool == "pong":
        _ = load_pong_acrossK(args.alignment_acrossK_file)

        #  major_mode_names = load_pong_acrossK(args.alignment_acrossK_file)
#           except Exception as e:
#             print(f"Error processing Pong alignment file {args.alignment_acrossK_file}: {e}")
#             raise
#         # print("Major mode names extracted from PONG alignment file:", major_mode_names)
    else:
        K_RE = re.compile(r"[kK]\s*_?\s*(\d+)")
        M_RE = re.compile(r"[mM]\s*_?\s*(\d+)")

        for filename in os.listdir(input_folder):
            if not filename.endswith(".Q"):
                continue

            input_path = os.path.join(input_folder, filename)
            stem = os.path.splitext(filename)[0]

            k_match = K_RE.search(stem)
            m_match = M_RE.search(stem)

            if not k_match:
                print(f" Skipping (no K found): {filename}")
                continue

            k_num = k_match.group(1)
            if m_match:
                m_num = m_match.group(1)
            else:
                reprun_match = re.search(r"reprun(\d+)", filename, re.IGNORECASE)
                m_num = reprun_match.group(1) if reprun_match else "1"

            output_filename = f"K{k_num}M{m_num}.csv"
            output_path = os.path.join(output_folder, output_filename)

            df = pd.read_csv(input_path, sep=r"\s+", header=None)

            df["name"] = [f"Ind{i+1}" for i in range(len(df))]
            df = df[["name"] + [c for c in df.columns if c != "name"]]

            num_clusters = df.shape[1] - 1
            df.columns = ["name"] + [f"Cluster{i+1}" for i in range(num_clusters)]

            if labels is not None:
                df["Population"] = labels
                df = df[["name", "Population"] + [c for c in df.columns if c not in ["name", "Population"]]]
                # print(f"populations added from {args.label_file}")

            df.to_csv(output_path, index=False)

    # Load data and generate HTML 
    data_json, alignment_json = load_files(args.processed_membership, args.alignment_file)

    import json

    try:
        mode_stats_json = "{}"
        if args.mode_stats and os.path.isfile(args.mode_stats):
            mode_stats_dict = {}
            df = pd.read_csv(args.mode_stats)
            for _, row in df.iterrows():
                mode_name = row["Mode"]
                size = row["Size"]
                mode_stats_dict[mode_name] = int(size)
            mode_stats_json = json.dumps(mode_stats_dict)
            
        html_content = generate_html_content(data_json, alignment_json, mode_stats_json)
        return html_content

    except Exception as e:
            print(f"Error loading mode stats from {args.mode_stats}: {e}")
            SystemExit("Aborted due to error in mode stats file.")
            # raise





# USER INTERFACE PART

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="KAlignedoscope: A tool for clustering and mapping genomic data."
    )

    
    parser.add_argument("--input", "-i", type=str, help="Input folder with .Q files")
    parser.add_argument("--label_file",  type=str, help="Optional file with individual labels to add as the second column", default=None)
    parser.add_argument('--processed_membership', type=str, required=True, help='Input folder containing the clustering result files.')
    parser.add_argument('--alignment_file', type=str, required=False, help='Input file containing the cluster alignment (from Clumppling).')
    parser.add_argument('--mode_stats', type=str, required=False, help='Input file containing mode statistics (Mode, Representative, Size, Cost, Performance).')
    parser.add_argument('--input_tool', type=str, choices=['clumppling', 'pong'], default='clumppling', help='Tool that generated the input files.')

    args = parser.parse_args()

    try:
        main(args)

    except (FileNotFoundError, ValueError) as e:
        print(f"\nPlease try again. {e}\n")
        raise SystemExit(1)


