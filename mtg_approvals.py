import pandas as pd

# Amending format of Columns, removing header rows and amending column names following review of CSV file.
mtg_approvals = pd.read_csv(r"C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\overall_loan_approvals_by_bank_by_year.csv", header=1, skiprows=[0, 1], names=["Year", "New Houses", "NH Value m's", "Other Houses", "OH Value m's", "Total No.", "Total Value"])
# Review of content of Dataset
print(mtg_approvals.shape)
print(mtg_approvals.columns)
print(mtg_approvals.info())
print(mtg_approvals.isna().sum())
# Note no missing values.

# Remove New home and other home values and counts as not analysing this subgroup.
mtg_approvals.drop(["New Houses", "NH Value m's", "Other Houses", "OH Value m's"], axis=1, inplace=True)

# Need to remove comma's from Value columns & Convert currency columns from Object dtypes to Float/Int dtypes
# Regex - Regular Expression - a special sequence of characters that defines a pattern for complex string - matching functionality.
mtg_approvals["Total Value"] = mtg_approvals["Total Value"].replace(',', '', regex=True).astype(float)
mtg_approvals["Total No."] = mtg_approvals["Total No."].replace(',', '', regex=True).astype(int)
print(mtg_approvals.info())

# Removing rows representing 2000 to 2009 as no comparable information on merging DF.
mtg_approvals = mtg_approvals.drop(mtg_approvals.index[:10])
print(mtg_approvals)

mtg_approvals.to_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\mtg_approvals_df.csv', index=False)
print(mtg_approvals)