import pandas as pd


df = pd.read_csv('attendance.csv')
df.head()

print(df.columns)
print(df.head())

# Convert 'Time' column to datetime, handling invalid formats
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time

# Print rows with invalid 'Time' values
invalid_times = df[df['Time'].isna()]
if not invalid_times.empty:
    print("Invalid time values found:")
    print(invalid_times)

# Drop rows with invalid 'Time' values (optional)
df = df.dropna(subset=['Time'])

# Remove rows with missing or invalid values in critical columns
df = df.dropna(subset=['NAME', 'Time', 'Date', 'Mode'])

# Print the cleaned DataFrame
print("Cleaned DataFrame:")
print(df.head())

df.to_csv('attendance.csv', index=False)