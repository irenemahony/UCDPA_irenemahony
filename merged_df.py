import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

house_sales = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\prop_sales_2010_2015.csv')
bank_loans = pd.read_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\mtg_approvals_df.csv')
print(house_sales.head())
print(bank_loans.head())

# Objective of merged info is to to see of All property transactions what portion was mortgage approved v's Cash- buyer (using Value & count)
# Removed New Home v's other as not going to look at this subgroup.
# Not using Concat as not common columns that would allow stack merge.
# No need to specify Inner Join as default setting of .merge function.
merged_df = house_sales.merge(bank_loans, on="Year", suffixes=('_house_sales', '_bank_loans'))
print(merged_df.head(6))
print(merged_df.columns)
print(merged_df.dtypes)

# Note the value currency is recorded differently in DF1 and DF2 - need to amend DF2 Total Value column (4141.8m) to mirror DF1 Column (5.1m)
merged_df["Total Value_bank_loans"] = merged_df["Total Value_bank_loans"]*1000000

# Fig 8: NP Array conversion to illustrate comparable transaction count & value - matplotlib
x = np.array(merged_df["Year"])
y0 = np.array(merged_df["Total No._house_sales"])
y1 = np.array(merged_df["Total No._bank_loans"])
y2 = np.array(merged_df["Total Value_house_sales"])
y3 = np.array(merged_df["Total Value_bank_loans"])

plt.style.use('seaborn-darkgrid')
fig, (ax, ax1) = plt.subplots(2, 1)
axs = (ax, ax1)

ax.plot(x, y0, color='purple', label="Total Houses Sold", linestyle='solid')
ax.plot(x, y1, color="red", label="Total Mortgage Drawdowns", linestyle='dashed')
ax1.plot(x, y2, color='purple', label="Total Value of Houses Sold", linestyle='solid')
ax1.plot(x, y3, color="red", label="Total Value Mortgage Drawdowns", linestyle='dashed')

ax.set(ylabel='No of Houses Sold')
ax1.set(xlabel='Year', ylabel="Value of House Sold (€ Trillion)")
ax.set_title("Total House Sales v's Mortgage drawdowns")
ax1.set_title("Total Value of House Sales v's Mortgage drawdowns")
ax.legend()
ax1.legend()
plt.show()

# Inserting Percentage information of mortgage over Total sales/transactions.
merged_df["Mortgage Value %"] = merged_df["Total Value_bank_loans"]/merged_df["Total Value_house_sales"]
merged_df["No of Mortgage %"] = merged_df["Total No._bank_loans"]/merged_df["Total No._house_sales"]
merged_df["Mortgage Value %"] = merged_df["Mortgage Value %"].map("{:.2%}".format)
merged_df["No of Mortgage %"] = merged_df["No of Mortgage %"].map("{:.2%}".format)
merged_df["Cash Buyer Value"] = merged_df["Total Value_house_sales"].sub(merged_df["Total Value_bank_loans"], axis=0)
merged_df["No of Cash Buyers"] = merged_df["Total No._house_sales"].sub(merged_df["Total No._bank_loans"], axis=0)
print(merged_df["Cash Buyer Value"]) # note due to decimal calculation differences - need to manually update df.loc[8]
print(merged_df.head(6))
print(merged_df.columns)
from decimal import Decimal
a = Decimal('5.098487933') # '5098487933.67001'
b = Decimal('4.141800000') # 141800000.00
print(a - b)# Correct answer €956,687,933.67001
merged_df.loc[8] = a-b
print(merged_df.head(6))