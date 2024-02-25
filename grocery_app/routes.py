from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm
from . import bcrypt, models
from grocery_app.extensions import app, db
from grocery_app.forms import SignUpForm
from flask_bcrypt import bcrypt
from grocery_app.forms import LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from grocery_app import bcrypt
from .login_manager import login_manager

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
@login_required
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(store)
        db.session.commit()
        flash('Store successfully created!', 'success')
        return redirect(url_for('main.store_detail', store_id=store.id))
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()
    if form.validate_on_submit():
        item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added to your cart!')
        return redirect(url_for('main.item_detail', item_id=item.id))
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash('Successfully updated store details!', 'success')
        return redirect(url_for('main.store_detail', store_id=store.id))
    return render_template('store_detail.html',form=form, store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url=form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        flash('Item details updated!', 'success')
        return redirect(url_for('main.item_detail', item_id=item.id))
    return render_template('item_detail.html', form=form, item=item)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign Up Successful!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    if item not in current_user.shopping_list_items:
        current_user.shopping_list_items.append(item)
        db.session.commit()
        flash('Item added to your shopping list!', 'success')
    return redirect(url_for('main.item_detail', item_id=item.id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list_items = current_user.shopping_list_items
    return render_template('shopping_list.html', shopping_list_items=shopping_list_items)

@main.route('/delete_item/<item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = GroceryItem.query.get(item_id)
    if item in current_user.shopping_list_items:
        current_user.shopping_list_items.remove(item)
        db.session.commit()
        flash('Item removed from your shopping list!', 'success')
    else:
        flash('Item not found in your shopping list!', 'error')
    return redirect(url_for('main.shopping_list'))