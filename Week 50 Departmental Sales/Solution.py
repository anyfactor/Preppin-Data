import pandas as pd

sheet_url = "https://docs.google.com/spreadsheets/d/15q9sIf3_heQqt-iGbL5HQFqXrE5FRADI/edit#gid=883438703"

# Easiest way to bring data directly from Google Sheets to Pandas
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
data = pd.read_csv(csv_export_url)


## Structuring the data ## 
# Very hacky
# I convert the dataframe to a list of list
# if the 3rd row, Salesperson doesn't exist that means it is a "data row"
# if it exists it is a salesperson information row

# This section essentially creates a lol where each child list contains an individual data from a salesperson
# While simultaneously creating a list
# This two list are sequential accurate
df_list = data.values.tolist()
salespersons = []
data_lol = [] # lol == list of lis
data_ind = []

for i in df_list:
    if type(i[2]) == str:
        salespersons.append(i)
        data_lol.append(data_ind)
        data_ind = []
    else:
        data_ind.append(i)

# Now I combine those two list into one lol
data_output = []
for table in data_lol:
    sales_data = salespersons[data_lol.index(table)]
    for row in table:
        row[2] = sales_data[2]
        row[7] = sales_data[7]
        data_output.append(row)

# I convert data_ouput lol (read, parent_data_lol)
parent_data = pd.DataFrame(data_output, columns = ['RowID', 'Date', 'Salesperson', 'Road', 'Gravel', 'Mountain', 'Total', 'YTD Total'])

# 
output_df = pd.DataFrame(columns=["Salesperson", "Date", "Bike Type", "Sales", "YTD Total"])
# Hold on to your hourses for this one...

for salesperson in salespersons:
    print(salespersons)
    # I again extract each individual salesperson data but this time in dataframe format
    salesperson_df = parent_data[parent_data["Salesperson"] == salesperson]
    # the constat ytd total
    ytd_total = salesperson_df["YTD Total"].iloc[0]
    
    # Melt function makes stacking super easy
    # id_vars are essentially what are static columns
    # value_vars will be combined into one column
    # I am sorting the new df by rowid then variable whihc is the bike_type column
    salesperson_data_melt = pd.melt(salesperson_df, id_vars=['RowID', 'Salesperson', 'Date'], value_vars=["Road", "Gravel", "Mountain"]).sort_values(by=['RowID', 'variable'])
    
    # Assigning the constant ytd. This statement adds a column with a constant value
    salesperson_data_melt["YTD Total"] = ytd_total
    # RowID isn't needed for output data
    # renaming them melt ouput column names
    salesperson_data_done = salesperson_data_melt.drop("RowID", axis=1).rename(columns={"variable": "Bike Type", "value": "Sales"})

    # adding each salesperson data to the output df
    output_df = output_df.append(salesperson_data_done)

# et viola!
print(output_df)