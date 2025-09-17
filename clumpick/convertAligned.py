import csv

input_file = r"C:/Users/13172/Downloads/my_d3_visualization/input_data/alignment_acrossK_1k/alignment_acrossK_rep.txt"   # or whatever your filename is
output_file = r"C:/Users/13172/Downloads/my_d3_visualization/input_data/1kg_alignment_costs.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    # Just keep modes and cost
    writer.writerow(["Mode1-Mode2", "Cost"])
    
    for row in reader:
        mode = row["Mode1-Mode2"]
        cost = row["Cost"]
        writer.writerow([mode, cost])