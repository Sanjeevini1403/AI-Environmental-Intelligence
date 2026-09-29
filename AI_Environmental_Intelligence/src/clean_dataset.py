import pandas as pd

# Load dataset
file_path = "data/Pune_SmartCity_Test_Dataset.csv"

df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["LASTUPDATEDATETIME"] = pd.to_datetime(
    df["LASTUPDATEDATETIME"],
    format="%d/%m/%y %H:%M",
    errors="coerce"
)

# Fill missing numerical values using median
numeric_columns = df.select_dtypes(include=["number"]).columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset shape:", df.shape)

# Save cleaned dataset
output_file = "data/pune_environmental_cleaned.csv"

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print("Saved at:", output_file)