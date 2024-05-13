# XML Data Scraper

This Python script scrapes XML data from a list of URLs stored in a CSV file, processes it, and saves the results into an Excel file.

## Installation

1. Clone this repository:

    ```
    git clone https://github.com/yourusername/xml-data-scraper.git
    ```

2. Install the required dependencies:

    ```
    pip install pandas requests beautifulsoup4
    ```

## Usage

1. Place your CSV file containing XBRL URLs and company names in the same directory as the script.

2. Run the script:

    ```
    python scraper.py
    ```

3. The scraped data will be saved in a directory named "Scrapped_Data" as an Excel file named "xml_data.xlsx".

## How it Works

1. **Importing Libraries**: The script imports necessary libraries such as Pandas, os, requests, BeautifulSoup, and datetime.

2. **Finding CSV File**: It looks for a CSV file in the current working directory. If exactly one CSV file is found, it loads it into a DataFrame (`df`).

3. **Data Cleaning**: Column names are cleaned by removing whitespace and '**' characters.

4. **Scraping XML Data**: The function `scrape_xml_data()` iterates over each row of the DataFrame (`df`). For each row, it retrieves the XBRL URL, sends a GET request to the URL, parses the XML content using BeautifulSoup, and extracts required elements like turnover, net worth, and emissions data. It then appends this data into a list (`scraped_data`).

5. **Saving Scraped Data**: After scraping data from all URLs, it converts the list (`scraped_data`) into a DataFrame (`scraped_df`). It sets the index starting from 1 and calculates the time taken for scraping. Then, it saves the DataFrame into an Excel file.

6. **Creating Directory**: It creates a directory named "Scrapped_Data" if it doesn't exist.

7. **Saving to Excel**: The scraped data is saved to an Excel file named "xml_data.xlsx" within the "Scrapped_Data" directory.
