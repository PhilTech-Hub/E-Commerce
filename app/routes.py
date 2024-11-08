# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Product, Order
from flask_login import login_required, current_user
from .utils import calculate_cart_total  # from utils
import paypalrestsdk


# Create the Blueprint
main = Blueprint('main', __name__)

paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
})

# Define a route for the home page
 # Ensure you have a home.html template in the templates folder
@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/simple_test')
def simple_test():
    return "This route works."

@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_seller:
        flash('Only sellers can add products!')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        product = Product(name=name, description=description, price=price, owner=current_user)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_product.html')



@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    order = Order(buyer_id=current_user.id, total_price=calculate_cart_total())
    db.session.add(order)
    db.session.commit()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(order.total_price),
                "currency": "KSH"
            },
            "description": f"Order {order.id}"
        }],
        "redirect_urls": {
            "return_url": url_for('main.payment_success', _external=True),
            "cancel_url": url_for('main.home', _external=True)
        }
    })

    if payment.create():
        return redirect(payment['links'][1]['href'])
    else:
        flash('Payment creation failed.')
        return redirect(url_for('main.home'))
