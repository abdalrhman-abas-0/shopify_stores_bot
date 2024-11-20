-- Active: 1730289566889@@127.0.0.1@5432@postgres
CREATE DATABASE shopify;

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    product_publish_date TIMESTAMP,
    product_vendor VARCHAR,
    product_type VARCHAR,
    product_tags JSON,
    product_options JSON,
    product_page VARCHAR,
    product_description VARCHAR,
    product_title VARCHAR
);

CREATE TABLE variants (
    product_id BIGINT REFERENCES products(product_id),
    variant_id BIGINT PRIMARY KEY,
    variant_title VARCHAR,
    variant_price REAL,
    variant_compare_at_price REAL,
    variant_sku VARCHAR,
    variant_created_at TIMESTAMP,
    variant_updated_at TIMESTAMP,
    variant_available BOOLEAN
);


CREATE TABLE images (
    image_id BIGINT PRIMARY kEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    variant_ids JSON,
    src VARCHAR,
    width INT,
    height INT
);


-- test the tables
select* from products;
select* from variants;
select* from images;


