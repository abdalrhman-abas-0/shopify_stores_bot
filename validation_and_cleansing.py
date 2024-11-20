"""validates the a product, its variants, and images and returns their dicts.

Typical usage example:

    product_dict = Products(
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
                
    variants_dict = Variants(
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
                
    images_dict = Images(
        id = image["id"],
        created_at = image.get("created_at"),
        updated_at = image.get("updated_at"),
        variant_ids = image.get("variant_ids"),
        src = image.get("src"),
        width = image.get("width"),
        height = image.get("height")
    ).as_dict()
    
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import re

@dataclass
class Products:
    """Represents a product with various attributes like vendor, type, tags, and more.

    Attributes:
        id (int): Unique identifier for the product.
        product_publish_date (Optional[str]): Date the product was published.
        product_vendor (Optional[str]): Vendor name for the product.
        product_type (Optional[str]): Type/category of the product.
        product_tags (Optional[list]): List of tags associated with the product.
        product_options (Optional[list]): List of options available for the product.
        product_page (Optional[str]): URL path for the product page.
        product_description (Optional[str]): Description of the product.
        product_title (Optional[str]): Title/name of the product.
        images_ids (Optional[list]): List of image IDs associated with the product.
    """
    id: int
    product_publish_date: Optional[str] = None
    product_vendor: Optional[str] = None
    product_type: Optional[str] = None
    product_tags: Optional[list] = None
    product_options: Optional[list] = None
    product_page: Optional[str] = None
    product_description: Optional[str] = None
    product_title: Optional[str] = None
    images_ids: Optional[list] = None

    def __post_init__(self):
        """Initializes additional processing for certain product attributes."""
        self.product_page = self.process_product_page()
        self.product_description = self.process_product_description()
        self.images_ids = self.process_images_ids()
        self.product_tags = self.process_product_tags()
        self.product_options = self.process_product_options()

    def as_dict(self):
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)

    def process_product_page(self) -> str:
        """Processes and constructs the full URL for the product page.

        Returns:
            str: Full URL for the product page.
        """
        return "https://:" + self.product_vendor + ".com" + "/products/" + self.product_page.replace(" ", "")

    def process_product_description(self) -> Optional[str]:
        """Removes HTML tags from the product description if it exists.

        Returns:
            Optional[str]: Cleaned product description.
        """
        if self.product_description:
            return re.sub(r"<\w+>|</\w+>", "", self.product_description)

    def process_images_ids(self) -> list:
        """Extracts IDs from the images list if it exists.

        Returns:
            list: List of image IDs.
        """
        if self.images_ids:
            return [i["id"] for i in self.images_ids]
        else:
            return []

    def process_product_tags(self) -> list:
        """Ensures product tags is a list.

        Returns:
            list: List of product tags.
        """
        if not self.product_tags:
            self.product_tags = []
        return self.product_tags

    def process_product_options(self) -> list:
        """Ensures product options is a list.

        Returns:
            list: List of product options.
        """
        if not self.product_options:
            return []
        return self.product_options

@dataclass
class Variants:
    """Represents a variant of a product, with attributes like price, SKU, and availability.

    Attributes:
        id (Optional[int]): Unique identifier for the variant.
        product_id (Optional[int]): ID of the product this variant belongs to.
        variant_title (Optional[str]): Title of the variant.
        variant_price (Optional[str]): Price of the variant.
        variant_compare_at_price (Optional[str]): Original price before discounts.
        variant_sku (Optional[str]): SKU of the variant.
        variant_created_at (Optional[str]): Date the variant was created.
        variant_updated_at (Optional[str]): Date the variant was last updated.
        variant_available (Optional[bool]): Availability status of the variant.
    """
    id: Optional[int] = None
    product_id: Optional[int] = None
    variant_title: Optional[str] = None
    variant_price: Optional[str] = None
    variant_compare_at_price: Optional[str] = None
    variant_sku: Optional[str] = None
    variant_created_at: Optional[str] = None
    variant_updated_at: Optional[str] = None
    variant_available: Optional[bool] = None

    def __post_init__(self):
        """Initializes additional processing for certain variant attributes."""
        self.variant_price = self.process_variant_price()
        self.variant_compare_at_price = self.process_variant_compare_at_price()

    def as_dict(self):
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)

    def process_variant_price(self) -> Optional[float]:
        """Converts variant price to a float if it exists.

        Returns:
            Optional[float]: Variant price as a float.
        """
        if self.variant_price:
            return float(self.variant_price)

    def process_variant_compare_at_price(self) -> Optional[float]:
        """Converts compare-at price to a float if it exists.

        Returns:
            Optional[float]: Compare-at price as a float.
        """
        if self.variant_compare_at_price:
            return float(self.variant_compare_at_price)

@dataclass
class Images:
    """Represents an image associated with a product or variant.

    Attributes:
        id (int): Unique identifier for the image.
        created_at (Optional[str]): Date the image was created.
        updated_at (Optional[str]): Date the image was last updated.
        variant_ids (Optional[list]): List of variant IDs the image is associated with.
        src (Optional[str]): Source URL of the image.
        width (Optional[int]): Width of the image in pixels.
        height (Optional[int]): Height of the image in pixels.
    """
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    variant_ids: Optional[list] = None
    src: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    def __post_init__(self):
        """Initializes additional processing for certain image attributes."""
        self.variant_ids = self.process_variant_ids()

    def as_dict(self):
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)

    def process_variant_ids(self) -> list:
        """Ensures variant IDs is a list.

        Returns:
            list: List of variant IDs associated with the image.
        """
        if self.variant_ids:
            return self.variant_ids
        else:
            return []
