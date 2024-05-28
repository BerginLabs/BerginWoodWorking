#!/usr/bin/env python3


import os

import pandas as pd
import numpy as np

from webapp import app, db
from webapp.models.products import Products, ProductImages, ProductCategories


def main():
    with app.app_context():
        print("[+] Dropping all tables.")
        db.drop_all()
        
        print("[+] Creating all new tables.")
        db.create_all()

        products_df = pd.read_csv(os.path.join('..', 'data', 'products-latest.csv'))
        product_images_df = pd.read_csv(os.path.join('..', 'data', 'products-images-latest.csv'))
        
        products_df = products_df.replace({np.nan: None})
        product_images_df = product_images_df.replace({np.nan: None})

        for index, row in products_df.iterrows():
            existing_product = Products.query.filter_by(sku=row['SKU']).first()
            if existing_product is None:
                product = Products(
                    sku=row['SKU'],
                    product_name=row['ProductName'],
                    product_category=row['ProductCategory'],
                    product_cost=row['ProductCost'],
                    suggested_sales_price=row['SuggestedSalesPrice'],
                    sales_tax_payable_based_on_suggested_sales_price=row['SalesTaxPayableBasedOnSuggestedSalesPrice'],
                    profit_based_on_suggested_sales_price=row['ProfitBasedOnSuggestedSalesPrice'],
                    percentage_of_profit=row['PercentageOfProfit'],
                    units_made=row['UnitsMade'],
                    units_sold=row['UnitsSold'],
                    units_available_for_sale=row['UnitsAvailableForSale'],
                    cost_of_units_made=row['CostOfUnitsMade'],
                    cost_of_inventory_available_for_sale=row['CostOfInventoryAvailableForSale'],
                    cogs_per_units_sold=row['COGSPerUnitsSold'],
                    money_collected_including_sales_tax=row['MoneyCollectedincludingSalesTax'],
                    date_sold=pd.to_datetime(row['DateSold']).date() if row['DateSold'] else None,
                    weight=row['Weight']
                )
                db.session.add(product)
            else:
                print(f"Skipping record import for sku: {row['SKU']}. Already Exists.")

        db.session.commit()
    
        for index, row in product_images_df.iterrows():
            row_sku = row['SKU']
            
            existing_product_image = ProductImages.query.filter_by(sku=row_sku).first()
            existing_product = Products.query.filter_by(sku=row_sku).first()
            
            if existing_product_image is None:

                product_image = ProductImages(
                    sku=row_sku,
                    product_id=existing_product.product_id,
                    encoded_image=row['Encoded_Photo']
                )
                db.session.add(product_image)
            
            else:
                print(f"Skipping product image with sku: {row_sku}. Already Exists.")
                continue
            
        db.session.commit()
        
        categories = {
            'Null': 'No Category Assigned',
            'None': 'No Category Assigned',
            'BAK': 'Wooden Baskets',
            'BOX': 'Wooden Boxes',
            'BRB': 'Bread Boards',
            'CGB': 'Cutting Boards',
            'CHB': 'Charcuterie Boards',
            'CHE': 'Cheese Boards',
            'COA': 'Coasters',
            'DRP': 'Dog Ramps',
            'OTH': 'Other',
            'SGN': 'Wooden Signs',
            'TRY': 'Wooden Trays',
            'WIC': 'Wine Caddies' 
        }
        
        for code, name in categories.items():
            existing_category = ProductCategories.query.filter_by(category_code=code, category_name=name).first()
            if existing_category is None:
                category = ProductCategories(
                    category_code=code,
                    category_name=name
                )
                db.session.add(category)
            else:
                print(f"Skipping category with code: {code} & name: {name}. Already Exists.")
                continue

        db.session.commit()
    return

if __name__ == '__main__':
    main()
