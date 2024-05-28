#!/usr/bin/env python3

import uuid

from webapp import db


class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    
    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)
    
    sku = db.Column(db.Integer)
    product_name = db.Column(db.String(255))
    product_category = db.Column(db.String(255))
    product_cost = db.Column(db.Numeric(10, 2))
    suggested_sales_price = db.Column(db.Numeric(10, 2))
    sales_tax_payable_based_on_suggested_sales_price = db.Column(db.Numeric(10, 2))
    profit_based_on_suggested_sales_price = db.Column(db.Numeric(10, 2))
    percentage_of_profit = db.Column(db.String(10))
    units_made = db.Column(db.Integer)
    units_sold = db.Column(db.Integer)
    units_available_for_sale = db.Column(db.Integer)
    cost_of_units_made = db.Column(db.Numeric(10, 2))
    cost_of_inventory_available_for_sale = db.Column(db.Numeric(10, 2))
    cogs_per_units_sold = db.Column(db.Numeric(10, 2))
    money_collected_including_sales_tax = db.Column(db.Numeric(10, 2))
    date_sold = db.Column(db.Date)
    weight = db.Column(db.Numeric(10, 2))
    product_images = db.relationship('ProductImages', backref='product', lazy=True)


class ProductImages(db.Model):
    __tablename__ = 'product_images'
    
    product_image_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    
    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)
    
    product_id = db.Column(db.String(36), db.ForeignKey('products.product_id'))
    sku = db.Column(db.Integer)
    encoded_image = db.Column(db.Text)


class ProductCategories(db.Model):
    __tablename__ = 'product_categories'
    
    product_category_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)

    created_date = db.Column(db.DateTime, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=True)

    category_code = db.Column(db.String(10))
    category_name = db.Column(db.String(255))
    encoded_image = db.Column(db.Text)
