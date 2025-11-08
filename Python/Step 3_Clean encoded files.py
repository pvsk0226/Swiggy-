import os
import csv

in_dir = r"C:\Pavithra\Swiggy\encoded_chunks"
out_dir = r"C:\Pavithra\Swiggy\clean_chunks"
os.makedirs(out_dir, exist_ok=True)

numeric_cols = ["rating", "rating_count", "cost"]

# helper function to clean numbers safely
def clean_number(value):
    import re
    cleaned = re.sub(r"[^0-9.]", "", str(value))
    return cleaned if cleaned else ""

# Process each encoded chunk file
for file_name in os.listdir(in_dir):
    if not file_name.endswith(".csv"):
        continue

    in_path = os.path.join(in_dir, file_name)
    out_path = os.path.join(out_dir, f"clean_{file_name}")

    print(f"Cleaning {in_path} -> {out_path}")

    with open(in_path, "r", encoding="utf-8", errors="ignore") as infile, \
         open(out_path, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        # Get index of numeric columns
        col_index = [header.index(c) for c in numeric_cols if c in header]

        for row in reader:
            for idx in col_index:
                row[idx] = clean_number(row[idx])
            writer.writerow(row)

    print(f" Finished cleaning {file_name}")

print("\nAll chunks cleaned safely without memory crash!")
