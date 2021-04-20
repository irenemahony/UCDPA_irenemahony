import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Values to be reflected in correct denomination in line with Total Value_house_sales
merged_df["Total Value_bank_loans"] = merged_df["Total Value_bank_loans"]*1000000

# Inserting Columns Percentage information of mortgage over Total sales/transactions.
merged_df["Mortgage Value %"] = merged_df["Total Value_bank_loans"]/merged_df["Total Value_house_sales"]
merged_df["No of Mortgage %"] = merged_df["Total No._bank_loans"]/merged_df["Total No._house_sales"]
merged_df["Mortgage Value %"] = merged_df["Mortgage Value %"].map("{:.2%}".format)
merged_df["No of Mortgage %"] = merged_df["No of Mortgage %"].map("{:.2%}".format)

# Inserting Column reflecting Non Mortgage/Cash Buyer from simple subtraction.
merged_df["Cash Buyer Value"] = merged_df["Total Value_house_sales"].sub(merged_df["Total Value_bank_loans"], axis=0)
merged_df["No of Cash Buyers"] = merged_df["Total No._house_sales"].sub(merged_df["Total No._bank_loans"], axis=0)

# Inserting Column reflecting Annual Average Price of Property & Average Mortgage amount.
merged_df["Average Yearly House Price"] = merged_df["Total Value_house_sales"]/merged_df["Total No._house_sales"]
merged_df["Average Yearly Mortgage Amount"] = merged_df["Total Value_bank_loans"]/merged_df["Total No._bank_loans"]
merged_df["Average Yearly Mortgage Amount"] = merged_df["Average Yearly Mortgage Amount"].round(2)
print(merged_df.head())
print(merged_df.columns)


# Fig 8: NP Array conversion to illustrate comparable transaction count & value - matplotlib
x = np.array(merged_df["Year"])
y0 = np.array(merged_df["Total No._house_sales"])
y1 = np.array(merged_df["Total No._bank_loans"])
y2 = np.array(merged_df["Total Value_house_sales"])
y3 = np.array(merged_df["Total Value_bank_loans"])
plt.style.use('seaborn-darkgrid')
fig, (ax, ax1) = plt.subplots(2, 1)
ax.plot(x, y0, color='purple', label="Total Houses Sold", linestyle='solid')
ax.plot(x, y1, color="red", label="Total Mortgage Drawdowns", linestyle='dashed')
ax1.plot(x, y2, color='purple', label="Total Value of Houses Sold", linestyle='solid')
ax1.plot(x, y3, color="red", label="Total Value Mortgage Drawdowns", linestyle='dashed')
ax.set(ylabel='No of Houses Sold')
ax1.set(xlabel="Year", ylabel="Value of House Sold (1 = 10 Billion)")
ax.set_title("Total House Sales v's Mortgage drawdowns")
ax1.set_title("Total Value of House Sales v's Mortgage drawdowns")
ax.legend()
ax1.legend()
plt.show()

# Fig 9 - Cash Purchased Property v's Mortgage Purchase
plt.style.use("ggplot")
ax.bar(merged_df["Year"], merged_df["No of Cash Buyers"], label="Cash Buyer", color="green")
ax.bar(merged_df["Year"], merged_df["Total No._bank_loans"], bottom=merged_df["No of Cash Buyers"], label="Mortgage Assisted", color="navy")
ax.set_xlabel("Year")
ax.set_ylabel("Total No. of Houses Sold")
ax.set_title("Cash Purchase v's Mortgage")
ax.legend()
plt.show()


# Fig 10 - Average Price of Properties per year & Average Mortgage Drawn.
y4 = np.array(merged_df["Average Yearly House Price"])
y5 = np.array(merged_df["Average Yearly Mortgage Amount"])
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.plot(x, y4, color='purple', label="Average Yearly House Price", linestyle='solid', marker="v")
ax.set_xlabel("Year")
ax.set_ylabel("Average House Price", color='purple')
ax.tick_params('y', color='purple')
ax2 = ax.twinx()
ax2.plot(x, y5, color="red", label="Average Yearly Mortgage Amount", linestyle='dashed', marker="o")
ax2.set_ylabel("Average Mortgage Amount", color="red")
ax.tick_params('y', color="red")
ax.legend(loc=4)
ax2.legend()
ax.set_title("Average Annual House Price & Average Mortgage Amount")
plt.show()

# Converting to CSV & exporting to .csv file
merged_df.to_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\merged_df.csv', index=False)
