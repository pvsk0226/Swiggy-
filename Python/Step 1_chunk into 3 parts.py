import pandas as pd
import os
import csv

input_file = r"C:\Pavithra\Swiggy\swiggy_cleaned.csv"   # update if needed
out_dir = r"C:\Pavithra\Swiggy\chunks"              # folder for chunk files
os.makedirs(out_dir, exist_ok=True)

chunk_size = 50000   # adjust: 50000, 20000, 10000 etc.
chunk_no = 1
saved_files = []


print("Starting chunking...")



for chunk in pd.read_csv(input_file, chunksize=chunk_size, iterator=True):
    out_path = os.path.join(out_dir, f"swiggy_part_{chunk_no:03d}.csv")
    chunk.to_csv(out_path, index=False)
    saved_files.append(out_path)
    print(f"Saved chunk {chunk_no}  {out_path}  (rows in this chunk: {len(chunk)})")
    chunk_no += 1

print(f"\nDone. Total chunks saved: {len(saved_files)}")

# Write a small manifest CSV listing the chunk files
manifest_path = os.path.join(out_dir, "chunks_manifest.csv")
with open(manifest_path, "w", newline="", encoding="utf-8") as mf:
    writer = csv.writer(mf)
    writer.writerow(["chunk_no", "file_path"])
    for i, f in enumerate(saved_files, start=1):
        writer.writerow([i, f])

print(f"Manifest saved {manifest_path}")
