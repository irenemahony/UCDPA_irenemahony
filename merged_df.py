import pandas as pd
import matplotlib.pyplot as plt

house_sales = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\prop_sales_2010_2015.csv')
bank_loans = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\mtg_approvals_df.csv')
print(house_sales.head())
print(bank_loans.head())

# Not using Concat as not common columns that would allow stack merge.
# No need to specify Inner Join as default setting of .merge function.
merged_df = house_sales.merge(bank_loans, on="Year", suffixes=('_house_sales', '_bank_loans'))
print(merged_df.head(6))
print(merged_df.columns)
print(merged_df.dtypes)

# Objective of merged info is to to see of All property transactions what portion was mortgage approved v's Cash- buyer (using Value & count)
# Rename columns to make more sense of combined dataframe - removed New Home v's other as not going to look at this subgroup.


# May be useful once Merged in Next Dataset
fig, ax = plt.subplots(sharey="Year")
ax.bar(merged_df["Year"], merged_df["Total No._house_sales"], color='purple')
ax.bar(merged_df["Year"], merged_df["Total No._bank_loans_"], bottom=merged_df["Total No._bank_loans_"], color="red")
ax.set_xlabel("Year")
ax.set_ylabel("No of Houses Sold")
ax.set_title("Property Sale Transactions supported by Mortgage")
plt.show()

