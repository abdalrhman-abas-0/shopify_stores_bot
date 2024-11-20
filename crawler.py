"""requests a shopify store and returns json response with the products

through the Requests_Handler class uses the config_store_url_and_name
method which takes the url of a store and returns the name of 
the stor and the url of it's products API, then the 
config_store_products_url will take the API url and add a pagination
 to the url to be used by the fetch_products_list which will make 
requests to this url and return a json response of the products 
on this store.

Typical usage example:
    
    req_handler = Requests_Handler()
    store_products_API, store_name = req_handler.config_store_url_and_name(store) 
    page_number = 1
    while True:
        store_products_API_paginated = req_handler.config_store_products_url(store_products_API, page_number)
        json_response = req_handler.fetch_products_list(store_products_API_paginated)
        row_products_list = json_response["products"]
        if len(row_products_list) > 0
            page_number += 1
        else:
            break
        
"""

from requests import session as r_session
import re
from time import sleep
import winsound

class Requests_Handler:
    """
    Handles HTTP requests using the `requests` library.

    Attributes:
        __session__: An instance of `requests.Session` to manage and persist settings across requests.
    """

    def __init__(self) -> None:
        """Initializes the Requests_Handler with a new session."""
        self.__session__ = r_session()
        
    def sound_alarm(self) -> None:
        """
        Plays an alarm sound using the `winsound` library.
        
        The alarm consists of a series of beeps with different frequencies and durations.
        """
        winsound.Beep(90, 100)
        winsound.Beep(1200, 100)
        winsound.Beep(1200, 100)
        winsound.Beep(1000, 300)
        winsound.Beep(900, 250)
        winsound.Beep(800, 1000) 

    def config_store_url_and_name(self, store: str) -> tuple[str, str]:
        """
        Configures the store URL and extracts the store name.

        Args:
            store: A string representing the store URL.

        Returns:
            A tuple containing the formatted store URL and store name.
        """
        store = store.strip("/")
        if "http" not in store:
            store_url = "https://" + store + "/"
        else:
            store_url  = store + "/"
        store_name = re.search(r"(?<=://).+(?=\.com)", store_url)[0]
        return store_url, store_name

    def config_store_products_url(self, store_url: str, page_number: int) -> str:
        """
        Configures the products URL for the given store and page number.

        Args:
            store_url: A string representing the store URL.
            page_number: An integer representing the page number.

        Returns:
            A string representing the complete products URL.
        """
        url = store_url + "products.json?limit=250&page=" + str(page_number)
        return url

    def fetch_products_list(self, url: str) -> list:
        """
        Fetches the list of products from the given URL.

        Args:
            url: A string representing the products URL.

        Returns:
            a json format response.
        
        Raises:
            ConnectionError: If there is a connection error during the request.
        """
        while True:
            try:
                response = self.__session__.get(url)
                break
            except:
                self.end_session()
                self.sound_alarm()
                print("Connection error!!")
                sleep(30)
        return response.json()
    
    def end_session(self) -> None:
        """Closes the current session."""
        self.__session__.close()