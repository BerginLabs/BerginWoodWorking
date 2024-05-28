#!/usr/bin/env python3


from webapp import app, db
from webapp.models.products import Products, ProductImages, ProductCategories

from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash


@app.route("/", methods=["GET"])
def index():
    coasters = Products.query.filter(Products.product_category == "COA").all()
    
    return render_template('index.html', coasters=coasters, search_enabled=False), 200


@app.route("/products", methods=["GET"])
def products():
    product_categories = ProductCategories.query.filter(
        ProductCategories.category_code != "null", 
        ProductCategories.category_code != "None"
    ).all()
    
    category_code = request.args.get('pcc', None)    
    if category_code:
        results = db.session.query(Products, ProductImages) \
            .join(ProductImages, Products.product_id == ProductImages.product_id) \
            .filter(Products.product_category == str(category_code)) \
            .all()              
    
    else:
        results = []

    return render_template(
        'products.html', 
        results=results,
        category_code=category_code, 
        product_categories=product_categories
    ), 200


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/admin", methods=['GET'])
def admin():
    product_data = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .all()

    return render_template(
        'admin.html', product_data=product_data
    ), 200


@app.route("/admin/view/<product_id>", methods=['GET'])
def view_product(product_id=None):
    query = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_id == product_id) \
        .first()  
    
    product, image = query[0], query[1]
    
    return render_template('view_product.html', product=product, image=image)


@app.route("/admin/remove/<product_id>", methods=['GET'])
def remove_product(product_id=None):
    try:
        product = db.session.query(Products).filter(Products.product_id == product_id).first()
        image = db.session.query(ProductImages).filter(ProductImages.product_id == product_id).first()
        
        if product:     
            if image:
                db.session.delete(image)
                
            db.session.delete(product)
            db.session.commit()
            
            flash("Successfully Deleted Product.", "success")
            
        else:
            flash("Product not found. Nothing to delete.", "danger")
            
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    
    return redirect(url_for('admin'))


@app.route('/admin/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id=None):
    query = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_id == product_id) \
        .first()  

    product, image = query[0], query[1]

    if request.method == 'POST':
        try:    
            product.sku = request.form['sku']
            product.product_name = request.form['product_name']
            product.product_category = request.form['product_category']
            product.product_cost = request.form['product_cost']
            product.suggested_sales_price = request.form['suggested_sales_price']
            product.sales_tax_payable_based_on_suggested_sales_price = request.form['sales_tax_payable_based_on_suggested_sales_price']
            product.profit_based_on_suggested_sales_price = request.form['profit_based_on_suggested_sales_price']
            product.percentage_of_profit = request.form['percentage_of_profit']
            product.units_made = request.form['units_made']
            product.units_sold = request.form['units_sold']
            product.units_available_for_sale = request.form['units_available_for_sale']
            product.cost_of_units_made = request.form['cost_of_units_made']
            product.cost_of_inventory_available_for_sale = request.form['cost_of_inventory_available_for_sale']
            product.cogs_per_units_sold = request.form['cogs_per_units_sold']
            product.money_collected_including_sales_tax = request.form['money_collected_including_sales_tax']
            product.date_sold = request.form['date_sold']
            product.weight = request.form['weight']
            
            db.session.commit()
            flash("Successfully Updated Product.", "success")
            return redirect(url_for('admin'))
        except Exception as err:
            db.session.rollback()
            flash("Unable to edit product.", "danger")

    return render_template('edit_product.html', product=product, image=image)
