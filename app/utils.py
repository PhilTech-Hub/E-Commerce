

def calculate_cart_total(cart_items):
    total = sum(item.price * item.quantity for item in cart_items)
    return total
