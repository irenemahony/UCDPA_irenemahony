import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


prop_sales = pd.read_csv(r"C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\House Sales PPR 2010 to 2021.csv", parse_dates=[0], index_col=[0], dtype=object)
# Review of content of Dataset
print(prop_sales.info())
print(prop_sales.dtypes)
print(prop_sales.describe())

# Updating Column Header titles
prop_sales.rename(columns={"Price (�)": "Price", "Property Size Description": "Size", "Description of Property": "Property Type", "Not Full Market Price": "Not Full Price"}, inplace=True)
print(prop_sales.columns)

# Date Column is index column from .csv import - need to amend title name and put in correct DF format.
print(prop_sales.rename_axis("Date", axis='index', inplace=True))
prop_sales.index = pd.to_datetime(prop_sales.index)
print(type(prop_sales.index[0]))

# Reviewing Missing Data within Dataset - Matplotlib
# print(prop_sales.fillna("NaN")
# prop_sales.isna().sum().plot(kind="bar", title="Missing Values", rot=45)
# plt.show()

# Removing Postal Code/Address_Location Data captured under County & Postal code & Property size data minimal.
print(prop_sales.drop(["Postal Code", "Size", "Address", "Not Full Price"], axis=1, inplace=True))
print(prop_sales.info())

# House Price currency symbol review - Value
spec_chars = ["!", "�", ",", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "–"]
for char in spec_chars:
    prop_sales["Price"] = prop_sales["Price"].str.replace(char, '', regex=True)

# Convert Sale price from String to float (including decimals)
prop_sales["Price"] = pd.to_numeric(prop_sales["Price"], errors='coerce')
print(prop_sales["Price"].dtype)

# Remove � from Property Type Column.
spec_chars = ["!", "�", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "–"]
for char in spec_chars:
    prop_sales["Property Type"] = prop_sales["Property Type"].str.replace(char, '', regex=True)
print(prop_sales["Property Type"])

# print("Time period from {} to {}".format(prop_sales.index.min(), prop_sales.index.max()))
# Created a column for year of sale to make use of more visualisations without having to reverse Date Indexing.
prop_sales["Year of Sale"] = prop_sales.index.year
print(prop_sales.head())

# Total Properties sold in Ireland From 2010 to 2021 = 466,646 total
total = prop_sales["Price"].value_counts().sum()
print(total)

# May be useful once Merged in Next Dataset
# fig, ax = plt.subplots()
# ax.bar(prop_sales["Year of Sale"], prop_sales["Year of Sale"], color='purple')
# ax.bar(prop_sales["Year of Sale"].value_counts(sort=False), prop_sales["Prop Type"], bottom=prop_sales["Prop Type"], color="red")
# ax.set_xlabel("Year")
# ax.set_ylabel("No of Houses Sold")
# ax.set_title("Annual Property Sales in Ireland")
# plt.show()


# VAT Exclusive Column indicates if New Build or secondhand - verifying prop type -demonstrating FOR LOOP /Conditional statement
new_homes = []
for value in prop_sales["VAT Exclusive"]:
    if value == "Yes":
        new_homes.append("New")
    else:
        new_homes.append("Secondhand")
prop_sales["Prop Type"] = new_homes
print(prop_sales.head())

# Converting column to boolean values to assist Visualisation of Second hand v's New Builds as a subgroup.
prop_sales["New Build?"] = np.where(prop_sales["VAT Exclusive"] == "Yes", True, False)
print(prop_sales.head())

# 392k Second Hand v's 75k New Build
quantity = prop_sales["Prop Type"].value_counts().to_frame()
print(quantity)

min_ = prop_sales['Price'].min()
print("Min Selling Price is :", min_)
avg_ = prop_sales['Price'].mean()
print("Average Selling Price is :", avg_)
median_ = prop_sales['Price'].median()
print("Median Selling Price is :", median_)
max_ = prop_sales['Price'].max()
print("Max Selling Price is :", max_)

# Fig 2: Sale Price Fluctuations over past 10 years - Price increasing again from 2018 onwards.
# Example of creating a function - reusing code.
# def plot_timeseries(axes, x, y, color, xlabel, ylabel):
# axes.plot(x, y, color=color)
# axes.set_xlabel(xlabel)
# axes.set_ylabel(ylabel, color=color)
# axes.tick_params('y', color=color)

# fig, ax = plt.subplots()
# plot_timeseries(ax, prop_sales.index, prop_sales["Price"], 'green', 'Time', 'House Price(€Millions)')
# plt.title("Trend of Property selling prices in Ireland 2010 to 2021")
# plt.grid(True)
# plt.show()

# Fig 3: Grouping & visualising Sales by County using Seaborn.
# sns.set(style="whitegrid")
# c = sns.catplot(x="County", data=prop_sales, kind="count", order=prop_sales["County"].value_counts().index)
# c.fig.suptitle("No. of Property Sales By County - 2010 to 2020", y=0.91)
# plt.xticks(rotation=45)
# plt.show()

# Fig 4: Most Expensive County to buy?
# plt.scatter(prop_sales.County, prop_sales.Price, color='purple')
# plt.title("Most Expensive County?")
# plt.ylabel("House Price (€ Millions)")
# plt.xticks(rotation=45)
# plt.show()

# Fig 5:
# Count of properties sold in Ireland on annual basis - 2020 dip (Pandemic) - 2021 Minimum data available.
# plt.style.use("ggplot")
# fig, ax = plt.subplots()
# ax = prop_sales["Year of Sale"].value_counts(sort=False).plot(kind='bar', color='purple', title="Volume of Annual House Sales", rot=45)
# ax.set_xlabel("Years")
# ax.set_ylabel("No. of Houses Sold")
# plt.show()

# Fig 6: Adding a third variable - Seaborn, point plot - Markers mean mean - removed Confidence interval (Facetgrid)
# Illustrating the Annual Average House Price in Ireland - across New Build & Secondhand subgroups
# sns.set_style('darkgrid')
# i = sns.catplot(x="Year of Sale", y="Price", data=prop_sales, hue="New Build?", kind="point", ci=None)
# i.fig.suptitle("Average House Price - New Build v's Second Hand", y=0.94)
# i.set(ylabel="Property Price (€)")
# plt.show()

# Fig 7
# Pandas DF Bar Plot - Illustration showing Majority Secondhand sale activity at 392,000 sales of total 466k
# prop_sales.set_index(prop_sales.index)['Prop Type'].value_counts().plot.bar()
# plt.ylabel("No of Houses Sold")
# plt.xlabel("Property Type")
# plt.title("Breakdown of Sales between New Build & Secondhand")
# plt.xticks(rotation=0)
# plt.show()

# Subsetting the existing DF to extract information relating to 2010 to 2015 in order to mirror timeline of merging dataset.
prop_sales_10_to_15 = prop_sales[(prop_sales["Year of Sale"] >= 2010) & (prop_sales["Year of Sale"] <= 2015)]
print(prop_sales_10_to_15.head())
print(prop_sales_10_to_15.tail())

# Extracting 2010 to 2015 Dafaframe (Grouped by years in order to merge with mtg loan approval dataset)
prop_sales_2010_2015 = pd.DataFrame(prop_sales_10_to_15.groupby(["Year of Sale"])["Price"].sum())
# Add Count column to reflect no of houses sold in any given year.
prop_sales_2010_2015["Count"] = prop_sales_10_to_15["Year of Sale"].value_counts(sort=True)
prop_sales_2010_2015["Price"].astype(int)
prop_sales_2010_2015["Count"].astype(int)
prop_sales_2010_2015.reset_index(level=0, inplace=True)
prop_sales_2010_2015.rename(columns={"Year of Sale": "Year"}, inplace=True)
print(prop_sales_2010_2015.head(6))
print(prop_sales_2010_2015.columns)
print(prop_sales_2010_2015.dtypes)

prop_sales_2010_2015.to_csv(r'C:\Users\paudi\Desktop\Data Analytics\.csv files UCD project\prop_sales_2010_2015.csv', index=False)
print(prop_sales_2010_2015)