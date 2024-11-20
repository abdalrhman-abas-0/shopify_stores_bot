# shopify_stores_bot

## Overview

- this project is designed to scrape a store products and save it's data into a PostgreSQL data base.
- it save the data into three tables products, variants, and images.

## Products info:

### Product table

- id
- product_publish_date
- product_vendor
- product_type
- product_tags
- product_options
- product_page
- product_description
- product_title
- images_ids

### Variants table

- id
- product_id
- variant_title
- variant_price
- variant_compare_at_price
- variant_sku
- variant_created_at
- variant_updated_at
- variant_available

## Images table

- id
- created_at
- updated_at
- variant_ids
- src
- width
- height

## Inputs:

- input the stores urls that you intend to scrape in the "stores_to_scrape.json" file and save it.

## Technologies Used

- **Python 3.x**: The main programming language used for the scraper.
- **Requests**: A light weight for Python used for making HTTP requests and return it's responses.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python, used for database interactions and storing the data.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL Database

### Setup

1. Clone the repository:

```bash
git clone https://github.com/abdalrhman-abas-0/shopify_stores_bot.git
cd shopify_stores_bot
```

2. Installing the necessary packages:

- to install the needed packages use the "requirements.txt" file :

```bash
pip install -r requirements.py
```

## File Structure

```bash
│
├── failed items/                # contains the jsonl files of the failed to save objects.
│   ├───images.jsonl
│   ├───products.jsonl
│   └───variants.jsonl   
├── .gitignore                   # contains the files/directories to be ignored by git.
├── crawler.py                   # makes the requests to a shopify store.
├── main.py                      # runs the project.
├── readme.md  
├── requirements.txt.py          # used to install all the necessary packages for the projects.
├── save_to_sql_db.py            # saves the scraped data to the sql data base.
├── scraper.py                   # extracts the products data from the responses.
├── shopify_db_creation.sql      # used to construct the database for save the extracted data.
├── stores_to_scrape.json        # contains the URLs of the stores to be scraped. 
└── validation_and_cleansing.py  # validates the scraped data.
```
