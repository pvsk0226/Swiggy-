import pandas as pd

cosine_master_path = r"C:\Pavithra\Swiggy\cosine_master.pkl"
cosine_master = pd.read_pickle(cosine_master_path)
print(f" Loaded cosine master shape: {cosine_master.shape}")
