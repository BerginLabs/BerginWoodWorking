#!/usr/bin/env python3


import os
from datetime import datetime

import pandas as pd
import numpy as np

from webapp import app, db
from webapp.models.products import Products, ProductImages, ProductCategories
from webapp.models.users import Users
from webapp.models.events import UpcomingEvents


def load_categories():
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
    
    print(f"[+] {len(categories)} categories found to import.")
    
    for code, name in categories.items():
        existing_category = ProductCategories.query.filter_by(category_code=code, category_name=name).first()
        
        if existing_category is None:
            
            category = ProductCategories(
                category_code=code,
                category_name=name,
                created_date=datetime.now(),
                updated_date=datetime.now()
            )
            db.session.add(category)
            
        else:
            print(f"[!] Skipping category with code: {code} & name: {name}. Already Exists.")
            continue

    db.session.commit()
    return True


def load_images():
    product_images_df = pd.read_csv(os.path.join('data', 'products-images-latest.csv'))
    product_images_df = product_images_df.replace({np.nan: None})
    
    print(f"[+] {len(product_images_df)} product image records found to import.")
    
    for _, row in product_images_df.iterrows():
        row_sku = row['SKU']
        
        existing_product_image = ProductImages.query.filter_by(sku=row_sku).first()
        existing_product = Products.query.filter_by(sku=row_sku).first()
        
        if existing_product_image is None:

            product_image = ProductImages(
                sku=row_sku,
                product_id=existing_product.product_id,
                encoded_image=row['Encoded_Photo'],
                created_date=datetime.now(),
                updated_date=datetime.now()
            )
            db.session.add(product_image)
        
        else:
            print(f"[!] Skipping product image with sku: {row_sku}. Already Exists.")
            continue

    db.session.commit()    
    return True


def load_products():
    products_df = pd.read_csv(os.path.join('data', 'products-5_28.csv'))
    products_df = products_df.replace({np.nan: None})
    
    print(f"[+] {len(products_df)} product records found to import.")
    
    for _, row in products_df.iterrows():
        existing_product = Products.query.filter_by(sku=row['SKU']).first()
        
        if existing_product is None:
            
            new_product = Products(
                created_date=datetime.now(),
                updated_date=datetime.now(),
                sku=row['SKU'],
                product_name=row['ProductName'],
                public_online_name=row['PublicOnlineName'],
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
            db.session.add(new_product)

        else:
            print(f"[!] Skipping product with sku: {row['SKU']}. Already Exists.")

    db.session.commit()  
    return True

def load_users():
    users_df = pd.read_csv(os.path.join('data', 'users.csv'))
    users_df = users_df.replace({np.nan: None})
    
    print(f"[+] {len(users_df)} user records found to import.")
    
    for _, row in users_df.iterrows():
        if row['first_name'].lower() == 'pat' and row['last_name'].lower() == 'bergin':
            new_user = Users(
                created_date=datetime.now(),
                updated_date=datetime.now(),
                user_email=row['user_email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone_number=row['phone_number'],
                address=row['address'],
                city=row['city'],
                state=row['state'],
                zip_code=row['zip_code'],
                email_verified=False,
                phone_verified=False,
                is_admin=True
            )

        else:
            new_user = Users(
                created_date=datetime.now(),
                updated_date=datetime.now(),
                user_email=row['user_email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone_number=row['phone_number'],
                address=row['address'],
                city=row['city'],
                state=row['state'],
                zip_code=row['zip_code'],
                email_verified=False,
                phone_verified=False,
                is_admin=False            
            )
            
        new_user.set_password(row['password'])
        db.session.add(new_user)
    
    db.session.commit()
    return True


def load_events():
    events_df = pd.read_csv(os.path.join('data', 'events.csv'))
    events_df = events_df.replace({np.nan: None})
    
    for _, row in events_df.iterrows():
        new_event = UpcomingEvents(
            created_date=datetime.now(),
            updated_date=datetime.now(),
            title=row['title'],
            date=datetime.strptime(row['date'], "%m/%d/%Y"),
            link=row['link'],
            description=row['description']
        )
        db.session.add(new_event)
    
    db.session.commit()
    return True


def main():
    print("[+] Beginning data import..")
    
    with app.app_context():
        print("[+] Dropping all tables.")
        db.drop_all()
        
        print("[+] Creating all new tables.")
        db.create_all()
        
        print("[+] Loading product categories.")
        load_categories()
        
        print("[+] Loading products.")
        load_products()

        print("[+] Loading product images.")
        load_images()
        
        print("[+] Loading test users.")
        load_users()
        
        print("[+] Loading Upcoming events.")
        load_events()
    
    print("[+] Data import complete.")
    return


if __name__ == '__main__':
    main()
