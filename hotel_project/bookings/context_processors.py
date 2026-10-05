from .cart import Cart

def cart_processor(request):
    # Get the cart from session safely, defaulting to empty structures
    cart = request.session.get('cart', {'rooms': {}, 'menu_items': {}})
    
    rooms_count = len(cart.get('rooms', {}))
    menu_count = len(cart.get('menu_items', {}))
    
    total_count = rooms_count + menu_count
    
    return {'cart_count': total_count}