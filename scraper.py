"""separates a products list into products, variants, and images lists.

through Products_Data_Extractors class it will connect to a the products,
variants, and images tables if they exist or create them and
stores the scraped products data in them.

Typical usage example:
    
    p_d_extractors = Products_Data_Extractors()
    products_list, variants_list, images_list = p_d_extractors.get_products_data_sql(row_products_list)
"""

import re
import json
from validation_and_cleansing import Products, Variants, Images

class Products_Data_Extractors:
    """
    Extracts and processes data for products, variants, and images.

    Attributes:
        __products_list (list): List of extracted products.
        __variants_list (list): List of extracted variants.
        __images_list (list): List of extracted images.
    """
    
    __products_list = []
    __variants_list = []
    __images_list = []

    def extract_variants(self, product: dict) -> None:
        """
        Extracts variant data from a product and appends it to the variants list.

        Args:
            product (dict): The product dictionary containing variant data.
        """
        variants = product.get("variants")
        for variant in variants:
            self.__variants_list.append(
                Variants(
                    id = variant["id"],
                    product_id = variant["product_id"],
                    variant_title = variant.get("title"),
                    variant_price = variant.get("price"),
                    variant_compare_at_price = variant.get("compare_at_price"),
                    variant_sku = variant["sku"],
                    variant_created_at = variant.get("created_at"),
                    variant_updated_at = variant.get("updated_at"),
                    variant_available = variant.get("available")
                ).as_dict()
            )

    def extract_images(self, product: dict) -> None:
        """
        Extracts image data from a product and appends it to the images list.

        Args:
            product (dict): The product dictionary containing image data.
        """
        images = product.get("images")
        if images is not None:
            for image in images:
                self.__images_list.append(
                    Images(
                        id = image["id"],
                        created_at = image.get("created_at"),
                        updated_at = image.get("updated_at"),
                        variant_ids = image.get("variant_ids"),
                        src = image.get("src"),
                        width = image.get("width"),
                        height = image.get("height")
                    ).as_dict()
                )

    def empty_all_lists(self) -> None:
        """
        Empties the products, variants, and images lists.
        """
        self.__products_list = []
        self.__variants_list = []
        self.__images_list = []

    def get_products_data_sql(self, row_products_list: list) -> tuple:
        """
        Extracts data for products, variants, and images from a list of raw product dictionaries.

        Args:
            row_products_list (list): List of raw product dictionaries.

        Returns:
            tuple: A tuple containing three lists - products, variants, and images.
        """
        for product in row_products_list:
            self.__products_list.append(
                Products(
                    id = product["id"],
                    product_publish_date = product.get("published_at"),
                    product_vendor = product.get("vendor"),
                    product_type = product.get("product_type"),
                    product_tags = product.get("tags"),
                    product_options = product.get("options"),
                    product_page = product.get("handle"),
                    product_description = product.get("body_html"),
                    product_title = product.get("title"),
                    images_ids = product.get("images")
                ).as_dict()
            )
            
            self.extract_variants(product)
            self.extract_images(product)
            
        return self.__products_list, self.__variants_list, self.__images_list
