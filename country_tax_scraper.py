from bs4 import BeautifulSoup
from requests import get
import json


# Function to scrape countries/taxes details from Trading Economics website
def scrape_table():
    res = get("https://tradingeconomics.com/country-list/sales-tax-rate")
    soup = BeautifulSoup(res.text, "lxml")

    country_set_1 = soup.select(".datatable-row")
    country_set_2 = soup.select(".datatable-row-alternating")

    country_list = []
    for index, country in enumerate(country_set_1):
        try:
            country_list.append(country_set_1[index].getText().split())
            country_list.append(country_set_2[index].getText().split())
        except:
            pass
    return country_list


# Function to modify country_list to contain only country names and tax rates
def get_country_info():
    country_list = scrape_table()
    for item in country_list:
        item.pop(-1)
        item.pop(-1)
        item.pop(-1)
    return country_list


# Function to join double country names
def final_country_list(country_list):
    return [[' '.join(c[:-1]), c[-1]] for c in country_list]


countries = get_country_info()
final_list = final_country_list(countries)

# Create JSON file
with open("country_tax.json", "w+") as file_handle:
    json.dump(final_list, file_handle)
