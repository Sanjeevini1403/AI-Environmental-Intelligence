import pandas as pd

file_path = "data/Pune_SmartCity_Test_Dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())