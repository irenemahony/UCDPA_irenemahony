import pandas as pd

house_sales = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\prop_sales_2010_2015.csv')
bank_loans = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\mtg_approvals_df.csv')
print(house_sales.head())
print(bank_loans.head())

# Not using Concat as not common columns that would allow stack merge.
# No need to specify Inner Join as default setting of .merge function.
merged_df = house_sales.merge(bank_loans, on="Year", suffixes=('_house_sales', '_bank_Loans'))
print(merged_df.head(6))
print(merged_df.columns)
print(merged_df.dtypes)

# Objective of merged info is to to see of All property transactions what portion was mortgage approved v's Cash- buyer (using Value & count)
# Rename columns to make more sense of combined dataframe - removed New Home v's other as not going to look at this subgroup.

