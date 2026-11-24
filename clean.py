# ### Reflection

#1. Filling missing values feels the most difficult because the average might not always be accurate. I would want to know why the information is missing before deciding what to replace it with.
#2. I think my comments explain most of my decisions, but it's important to explain why I made them. For example, I removed rows missing order IDs because those orders could not be properly identified.
#3. I was surprised by how many different issues the dataset had, including missing values, incorrect data types, and unusual quantities. It showed me how important it is to check data before analyzing it.


# -- exercise 1: inspect --

import pandas as pd

# Load the messy sales dataset
df = pd.read_csv("data/messy_sales.csv")

# Display information about the dataset
print(df.info())

# Display missing values in each column
print(df.isnull().sum())

# Data Quality Issues:
# 1. The price column contains missing values.
# 2. The quantity column is stored as an object instead of a numeric data type.
#3. The customer column has missing entries.



# -- exercise 2: standardize column names --

# Convert column names to lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Print updated column names
print(df.columns.tolist())


# -- exercise 3: handle missing values --

# Print shape before removing rows
print("Shape before:", df.shape)

# Drop rows missing essential identifiers
df = df.dropna(subset=["order_id", "order_date"])

# Fill missing numeric values with their column means
numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].mean())

# Print shape after removing rows
print("Shape after:", df.shape)

# Check remaining missing values
print(df.isnull().sum())


# -- exercise 4: fix types --

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Print the number of dates that became NaT
print("Dates converted to NaT:", df["order_date"].isna().sum())

# Convert unit_price to float after removing dollar signs and commas
df["unit_price"] = df["unit_price"].str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

# Convert quantity_sold to integer
df["quantity_sold"] = df["quantity_sold"].astype(int)

# Calculate revenue
df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)

# Display data types
print(df.dtypes)


# -- exercise 5: check duplicates --

# Count duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# Remove duplicate rows if they exist
if df.duplicated().sum() > 0:
    df = df.drop_duplicates()

# Print updated shape
print("Shape after removing duplicates:", df.shape)


# -- exercise 6: describe --

# Display descriptive statistics
print(df.describe())

# Suspicious statistics and business explanations:

#1. [Identify a suspicious statistic from describe() and explain why it looks unusual.]
#2. [Identify another suspicious statistic and suggest a possible business explanation.]

#A quantity_sold of 9,999 is a placeholder rather than a real order,
#so those rows should be removed from the dataset.
#Negative revenues are kept because they represent customer returns.


# Remove rows where quantity_sold equals 9,999
df = df[df["quantity_sold"] != 9999]

# Print updated shape
print("Shape after removing placeholder quantities:", df.shape)


# -- exercise 7: save --

# Export cleaned data to CSV
df.to_csv("data/clean_sales.csv", index=False)

# Reload the cleaned CSV file
df = pd.read_csv("data/clean_sales.csv")

# Display information about the reloaded data
print(df.info())

# Reload CSV with order_date recognized as datetime
df = pd.read_csv("data/clean_sales.csv", parse_dates=["order_date"])

# Check data types again
print(df.info())

