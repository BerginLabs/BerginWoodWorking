#!/usr/bin/env python3

import random
from datetime import datetime

from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash

from flask_login import login_user, logout_user, login_required, current_user

from webapp import app, db
from webapp.models.products import Products, ProductImages, ProductCategories
from webapp.models.users import Users
from webapp.models.events import UpcomingEvents


@app.route("/", methods=["GET"])
def index():
    search_enabled = False
    
    upcoming_events = UpcomingEvents.query.order_by(UpcomingEvents.date).all()
    
    coasters = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_category == "COA") \
        .all()              
    coaster_highlight = coasters[random.randint(0, len(coasters) - 1)] if coasters else None
    
    boards = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_category == "CGB") \
        .all()              
    board_highlight = boards[random.randint(0, len(boards) - 1)] if boards else None

    return render_template(
        'index.html', 
        coasters=coasters, 
        coaster_highlight=coaster_highlight,
        board_highlight=board_highlight,
        upcoming_events=upcoming_events, 
        search_enabled=search_enabled
    ), 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        
        if Users.query.filter_by(user_email=user_email).first():
            flash("Email address already exists. Please use forgot password.", "danger")
            return redirect(url_for('register'))

        new_user = Users(
            user_email=user_email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            created_date = datetime.now(),
            updated_date = datetime.now()
        )
        
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']
        
        user_to_login = Users.query.filter_by(user_email=user_email).first()
        
        if user_to_login and user_to_login.check_password(password):
            login_user(user_to_login)
            flash('Login successful.', "success")
            return redirect(url_for('index'))
        
        else:
            flash('Invalid email address or password.', "danger")
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    flash('You have successfully been logged out.', "success")
    return redirect(url_for('index'))


@app.route('/users/profile', methods=['GET', 'POST'])
def my_profile():
    flash("this page is still in development.", "warning")
    
    profile = Users.query.filter(Users.user_id == current_user.user_id).first()
    if request.method == "POST":
        profile.first_name = request.form['first_name']
        profile.last_name = request.form['last_name']
        profile.phone_number = request.form['phone_number']
        profile.user_email = request.form['user_email']
        db.session.commit()
        
        flash("Successfully updated profile.", "success")
        return redirect(url_for('my_profile'))

    return render_template("my_profile.html", me=profile)


@app.route("/products", methods=["GET"])
def products():
    product_categories = ProductCategories.query.filter(
        ProductCategories.category_code != "null", 
        ProductCategories.category_code != "None"
        ) \
        .order_by(ProductCategories.category_name) \
        .all()
    
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

@app.route("/products/view/<product_id>", methods=['GET'])
def product_details(product_id=None):   
    query = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_id == product_id) \
        .first()

    product, image = query[0], query[1]
    
    product_category = db.session.query(ProductCategories) \
        .filter(ProductCategories.category_code == product.product_category) \
        .first()
    
    return render_template('product_details.html', product=product, image=image, product_category=product_category)

@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/cart")
def cart():
    flash("this page is still in development.", "warning")
    return render_template('cart.html')


@app.route("/admin", methods=['GET'])
@login_required
def admin():
    profile = Users.query.filter(Users.user_id == current_user.user_id, Users.is_admin == True).first()    
    
    if not profile:
        return redirect( url_for('index') )
    
    product_data = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .all()
        
    user_data = Users.query.all()
    
    return render_template(
        'admin.html', product_data=product_data, user_data=user_data
    ), 200


@app.route("/admin/view/<product_id>", methods=['GET'])
@login_required
def view_product(product_id=None):
    profile = Users.query.filter(Users.user_id == current_user.user_id, Users.is_admin == True).first()    
    
    if not profile:
        return redirect( url_for('index') )
    
    query = db.session.query(Products, ProductImages) \
        .join(ProductImages, Products.product_id == ProductImages.product_id) \
        .filter(Products.product_id == product_id) \
        .first()  
    
    product, image = query[0], query[1]
    
    return render_template('view_product.html', product=product, image=image)


@app.route("/admin/remove/<product_id>", methods=['GET'])
@login_required
def remove_product(product_id=None):
    profile = Users.query.filter(Users.user_id == current_user.user_id, Users.is_admin == True).first()    
    
    if not profile:
        return redirect( url_for('index') )
    
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
@login_required
def edit_product(product_id=None):
    profile = Users.query.filter(Users.user_id == current_user.user_id, Users.is_admin == True).first()    
    
    if not profile:
        return redirect( url_for('index') )
    
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
