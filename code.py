
# Importing all libraries
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#########################################################################################################
# Get the current working directory
cwd = os.getcwd()

# Find the CSV file in the same directory
csv_files = [f for f in os.listdir(cwd) if f.endswith('.csv')]

if len(csv_files) == 1:
    csv_file = csv_files[0]
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    print(f"Data loaded from {csv_file} into DataFrame df.")
    
else:
    print("Error: Either no CSV file or multiple CSV files found in the same directory.")
#########################################################################################################
# Remove whitespace characters from column names
df.columns = df.columns.str.strip()

# Remove whitespace characters and '**' from column names
df.columns = df.columns.str.strip().str.replace('**', '')

#########################################################################################################
def scrape_xml_data(df):
    start_time = datetime.now()
    scraped_data = [] # list to store entire DF context
    # When you iterate over a DF with `df.iterrows()`, each iteration gives you a tuple containing an index & a Series representing the row.
    for index, row in df.iterrows(): 
        company_start_time = datetime.now()
        xbrl_url = row['XBRL']
        if pd.notnull(xbrl_url):
            try:
                # This sends a GET request to the XBRL URL using the requests.get() function, with a custom User-Agent header
                response = requests.get(xbrl_url, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()
                
                # Convert XML content to BeautifulSoup object using lxml-xml parser
                soup = BeautifulSoup(response.content, 'lxml-xml')
                
                # Extract required elements
                turnover = soup.find('Turnover').text.strip() if soup.find('Turnover') else None
                net_worth = soup.find('NetWorth').text.strip() if soup.find('NetWorth') else None
                
                # Extract DCY and DPY values
                dcy_total_scope1_emissions = soup.find('TotalScope1Emissions', contextRef='DCYMain').text.strip() if soup.find('TotalScope1Emissions', contextRef='DCYMain') else None
                dcy_unit_of_scope1_emissions = soup.find('UnitOfTotalScope1Emissions', contextRef='DCYMain').text.strip() if soup.find('UnitOfTotalScope1Emissions', contextRef='DCYMain') else None
                dcy_total_scope2_emissions = soup.find('TotalScope2Emissions', contextRef='DCYMain').text.strip() if soup.find('TotalScope2Emissions', contextRef='DCYMain') else None
                dcy_unit_of_scope2_emissions = soup.find('UnitOfTotalScope2Emissions', contextRef='DCYMain').text.strip() if soup.find('UnitOfTotalScope2Emissions', contextRef='DCYMain') else None
                
                dpy_total_scope1_emissions = soup.find('TotalScope1Emissions', contextRef='DPYMain').text.strip() if soup.find('TotalScope1Emissions', contextRef='DPYMain') else None
                dpy_unit_of_scope1_emissions = soup.find('UnitOfTotalScope1Emissions', contextRef='DPYMain').text.strip() if soup.find('UnitOfTotalScope1Emissions', contextRef='DPYMain') else None
                dpy_total_scope2_emissions = soup.find('TotalScope2Emissions', contextRef='DPYMain').text.strip() if soup.find('TotalScope2Emissions', contextRef='DPYMain') else None
                dpy_unit_of_scope2_emissions = soup.find('UnitOfTotalScope2Emissions', contextRef='DPYMain').text.strip() if soup.find('UnitOfTotalScope2Emissions', contextRef='DPYMain') else None
                
                # Append data to list----> Creates list of dic eg --> list = [{col1:x,col2:y},{col1:s,col2:f},{col1:j,col2:g},....{}] where each ele of list is unique row of df
                scraped_data.append({
                    'Company': row['COMPANY'],
                    'Turnover': turnover,
                    'NetWorth': net_worth,
                    'DCY TotalScope1Emissions': dcy_total_scope1_emissions,
                    'DCY UnitOfTotalScope1Emissions': dcy_unit_of_scope1_emissions,
                    'DCY TotalScope2Emissions': dcy_total_scope2_emissions,
                    'DCY UnitOfTotalScope2Emissions': dcy_unit_of_scope2_emissions,
                    'DPY TotalScope1Emissions': dpy_total_scope1_emissions,
                    'DPY UnitOfTotalScope1Emissions': dpy_unit_of_scope1_emissions,
                    'DPY TotalScope2Emissions': dpy_total_scope2_emissions,
                    'DPY UnitOfTotalScope2Emissions': dpy_unit_of_scope2_emissions
                })
                
                print(f"Scraped data for {index+1}.{row['COMPANY']}. Time taken: {(datetime.now() - company_start_time).total_seconds()} seconds") 
            except requests.exceptions.RequestException as e:
                print(f"Error scraping data for {index+1}.{row['COMPANY']}: {e}")
    
    # Convert scraped data to DataFrame
    scraped_df = pd.DataFrame(scraped_data)
    scraped_df.index = scraped_df.index + 1  # Start index from 1
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print(f"Total time taken: {total_time} seconds")
    return scraped_df

if __name__ == "__main__":
    # Assuming df is your DataFrame with the XBRL URLs and COMPANY names
    scraped_df = scrape_xml_data(df)
# Specify the directory path
dir_path = '.Scrapped_Data'

# Check if the directory exists, if not, create it
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
#########################################################################################################
# Save the DataFrame to an Excel file
excel_file_path = os.path.join(dir_path, 'xml_data.xlsx')
scraped_df.to_excel(excel_file_path, index=False)
print(f"XML data saved to: {excel_file_path}") 
