# Import libraries
import pandas as pd
import re

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data.csv")

print("Original Dataset:\n")
print(df)

# -----------------------------
# DATA QUALITY REPORT (BEFORE)
# -----------------------------
print("\n--- DATA QUALITY REPORT (BEFORE CLEANING) ---")
print(f"Total Rows: {len(df)}")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Duplicate Rows: {df.duplicated().sum()}")

# -----------------------------
# CLEANING PROCESS
# -----------------------------

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Clean whitespace from strings
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# 3. Replace empty strings with NaN
df.replace("", pd.NA, inplace=True)

# 4. Convert Age and Salary to numeric
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# 5. Fill missing Age with average
df["Age"].fillna(df["Age"].mean(), inplace=True)

# 6. Fill missing Salary with average
df["Salary"].fillna(df["Salary"].mean(), inplace=True)
# Round salary to 2 decimal places and convert to integer
df["Salary"] = df["Salary"].round(2).astype(int)

# 7. Fill missing Email with placeholder
df["Email"].fillna("unknown@email.com", inplace=True)

# -----------------------------
# EMAIL VALIDATION
# -----------------------------
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))

df["Email_Valid"] = df["Email"].apply(validate_email)

# -----------------------------
# SORT DATA (HIGH TO LOW SALARY)
# -----------------------------
df = df.sort_values(by="Salary", ascending=False)

# -----------------------------
# DATA QUALITY REPORT (AFTER)
# -----------------------------
print("\n--- DATA QUALITY REPORT (AFTER CLEANING) ---")
print(f"Total Rows: {len(df)}")
print(f"Missing Values:\n{df.isnull().sum()}")

# -----------------------------
# INVALID EMAIL REPORT
# -----------------------------
print("\n--- INVALID EMAILS ---")
invalid_emails = df[df["Email_Valid"] == False]
print(invalid_emails if not invalid_emails.empty else "No invalid emails found")

# -----------------------------
# DATA QUALITY SCORE
# -----------------------------
total_cells = df.size
missing_cells = df.isnull().sum().sum()

quality_score = ((total_cells - missing_cells) / total_cells) * 100

print(f"\nData Quality Score: {quality_score:.2f}%")

# -----------------------------
# SUMMARY INSIGHTS
# -----------------------------
print("\n--- SUMMARY ---")
print(f"Average Age: {df['Age'].mean():.2f}")
print(f"Average Salary: {df['Salary'].mean():.2f}")

# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
df.to_csv("cleaned_data.csv", index=False)

print("\nCleaned dataset saved as cleaned_data.csv")