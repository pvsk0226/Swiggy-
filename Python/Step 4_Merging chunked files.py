import os
import glob

# input and output folders
in_dir = r"C:\Pavithra\Swiggy\encoded_chunks"   # or "clean_chunks" if you cleaned
out_path = r"C:\Pavithra\Swiggy\swiggy_merged.csv"

# get all chunk files sorted
files = sorted(glob.glob(os.path.join(in_dir, "*.csv")))

print(f"Found {len(files)} chunk files to merge...\n")

# remove old merged file if exists
if os.path.exists(out_path):
    os.remove(out_path)

header_written = False

with open(out_path, "w", encoding="utf-8", newline="") as outfile:
    for file in files:
        print(f"Appending {file} ...")
        with open(file, "r", encoding="utf-8", errors="ignore") as infile:
            header = infile.readline()
            if not header_written:
                outfile.write(header)
                header_written = True
            # write all remaining lines except the header
            for line in infile:
                outfile.write(line)

print(f"\n All chunks merged successfully into: {out_path}")
