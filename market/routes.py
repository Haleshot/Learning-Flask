from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import Register_Form, Login_Form, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/') # Defining a decorator in python before the function. This helps us in calling functions.
@app.route('/home') # We can have multiple app routes pointing to particular homepage/website. In this case, both websites with and without home display the same Home page/website.
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required # Mentioning that login is required before the market route is called to ensure user is logged in before getting redirected to the market page.
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Item purchasing block:
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object): # Checks from function present in models.py User class.
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you do not have enough money to purchase {p_item_object.name}", category='danger')


        # Selling Item Block:
        sold_item =   request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to the market for {s_item_object.price}$", category='success')

            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET": # To ensure that the resubmission confirmation popup doesn't appear everytime we try to refresh our webpage.
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register_Form()
    if form.validate_on_submit(): # Checks if user has clicked on the submit button.
        user_to_create = User(username=form.username.data, # Collecting the text entered by user in the text box in webpage.
                              email_address=form.email_address.data,
                              password=form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account Created Successfully! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page')) # Redirecting the user after they click on the submit button.
    form.errors # If the validations in the forms.py fails, those errors will be stored in forms.errors. It is a dictionary.
    if form.errors != {}: # If there are no errors stored in the file.
        for err_msg in form.errors.values():
            # print("Error message : ", err_msg), if you want to display the validation error in your terminal server running which is not recommended as you want to display the error message to the user.
            # flash("Error message : ", err_msg, category='danger') # Flash shows the error message directly on the webpage running.
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = Login_Form()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as {attempted_user.username}", category='success')
            return redirect(url_for('market_page'))

        else:
            flash("Username and Password do not match! Please try again!", category='danger')


    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))