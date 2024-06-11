#!/usr/bin/env python3

import os
import shopify
import pandas as pd


class Config:
    SHOPIFY_CLIENT_ID = os.getenv('SHOPIFY_CLIENT_ID')
    SHOPIFY_CLIENT_SECRET = os.getenv('SHOPIFY_CLIENT_SECRET')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
    SHOPIFY_API_VERSION = "2024-01"
    SHOPIFY_STORE_NAME = '27000d-f5.myshopify.com'
    SHOPIFY_URL = f"https://{SHOPIFY_STORE_NAME}/admin"
    PRODUCT_DATA = os.path.join("data", "shopify-products-with-images.csv")


config = Config()

session = shopify.Session(
    config.SHOPIFY_URL,
    config.SHOPIFY_API_VERSION, 
    config.SHOPIFY_ACCESS_TOKEN
)

def create_product(product_data):    
    new_product = shopify.Product()

    new_product.title = product_data['Title']
    new_product.body_html = product_data['Body']
    new_product.vendor = product_data['Vendor']
    new_product.product_type = product_data['Type']
    new_product.sku = int(product_data['SKU'])
    new_product.price = int(product_data['Variant Price'])
    
    requires_shipping = True if product_data.get('Variant Taxable') == True else False
    taxable = product_data.get('Variant Taxable', False)
    
    weight = product_data.get('Variant Weight Unit')
    weight = weight if weight.is_integer() else 0
    
    units_avail = product_data.get("Variant Inventory Qty")
    units_avail = units_avail if units_avail is not None else 0

    variant = shopify.Variant({
        "price": product_data['Variant Price'],
        "sku": int(product_data['SKU']),
        "requires_shipping": requires_shipping,
        "taxable": taxable,
        "weight": weight,
        "units_available": units_avail
    })

    new_product.variants = [variant]    
    new_product.save()

    filename = f"{int(product_data['SKU'])}.png"
    file_data = product_data["Encoded_Photo"]
    if isinstance(file_data, str):
    
        if len(file_data) > 0:        
            image = shopify.Image({
                "attachment": file_data,
                "filename": filename,
                "position": 1,
                "product_id": new_product.id
            })
            image.save()
        else:
            print(f"[!] Skipping image upload for sku: {new_product.sku}. No image content available.")
            
    else:
        print(f"[!] Skipping image upload for sku: {new_product.sku}. Image content not a string.")


if __name__ == '__main__':
    print("[+] Starting Shopify Product Upload.")
    
    products_df = pd.read_csv(config.PRODUCT_DATA)
    products_df.rename(columns={'Variant SKU': 'SKU'}, inplace=True)
    products_df['Vendor'] = "Bergin Woodworking"
    
    shopify.ShopifyResource.activate_session(session)

    ctr = 0
    for index, product in products_df.iterrows():
        ctr += 1
        
        this_product = product.to_dict()
        print(f"[+] Uploading: #{ctr} - SKU={int(this_product['SKU'])} | TITLE={this_product['Title']} | QTY={this_product['Variant Inventory Qty']}")
        
        create_product(product_data=this_product)

    shopify.ShopifyResource.clear_session()
    print("[+] Upload Complete.")
