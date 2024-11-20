from crawler import Requests_Handler
from scraper import Products_Data_Extractors
from save_to_sql_db import Write_to_DB
from dotenv import load_dotenv, dotenv_values
import os
import json

if __name__ == "__main__":
    # Load database credentials from .env file
    db_info = dotenv_values(".env")

    # Initialize instances for data extraction, request handling, and database insertion
    p_d_extractors = Products_Data_Extractors()
    req_handler = Requests_Handler()
    write_to_db = Write_to_DB(
        db_info["db_user_name"], 
        db_info["db_password"], 
        db_info["db_port"], 
        db_info["db_name"]
        )
    
    # Load list of stores to scrape from JSON file
    with open("stores_to_scrape.json", "r") as f:
        stores_list = json.load(f)
    
    all_stores_scraping_summary = ""
    # Iterate over each store in the list 
    for store in stores_list: 
        # Configure the store's URL and name
        store_products_API, store_name = req_handler.config_store_url_and_name(store) 
        
        print(f"\nstores index: <<{stores_list.index(store)+1}: {len(stores_list)}>>")
        store_url_str = f"store: {store_name}\nurl: {store_products_API}"
        print(store_url_str)
        
        page_number = 1
        # Iterate through paginated product lists
        
        # tracks the number of products scraped from a store
        total_products = 0
        
        while True:
            # Configure the URL for the current page and fetch product data
            store_products_API_paginated = req_handler.config_store_products_url(store_products_API, page_number)
            json_response = req_handler.fetch_products_list(store_products_API_paginated)
            row_products_list = json_response["products"]
            
            # Check if products are available on the page
            if len(row_products_list) > 0:
                # Extract product data and prepare for database insertion
                products_list, variants_list, images_list = p_d_extractors.get_products_data_sql(row_products_list)
                
                # counting the scraped products
                total_products += len(products_list)
                
                # Insert extracted data into database tables
                write_to_db.insert_into_table("products", products_list)
                write_to_db.insert_into_table("variants", variants_list)
                write_to_db.insert_into_table("images", images_list)
                
                # Clear data lists for the next page of products
                p_d_extractors.empty_all_lists()
                
                print(f"current page: {page_number}")
                page_number += 1
                
            else:
                # save store scraping data to store summary
                all_stores_scraping_summary += f"{'-'*50}\n{store_products_API}\npages scraped: {page_number}\nproducts scraped: {total_products}\n{'-'*50}\n"
                # Exit pagination if no products are found on the current page
                break
        # Clear console output (for Windows systems)
        os.system("cls")
        
    # Terminate database connection and end HTTP session
    write_to_db.terminate_connection()
    req_handler.end_session()
    
    print('scraping is concluded successfully.')
    print(f"scraping summary:\n{all_stores_scraping_summary}")
    print('*please empty the .jsonl files in the "filed items" folder before the running the scraper again.')
