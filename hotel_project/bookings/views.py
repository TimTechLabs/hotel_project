from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from .models import MenuItem, Order, Room

def home(request):
    featured_rooms = Room.objects.all()[:3]
    return render(request, 'bookings/home.html', {'featured_rooms': featured_rooms})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'bookings/room_list.html', {'rooms': rooms})

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu_list.html', {'menu_items': menu_items})

def room_add_to_cart(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        quantity = request.POST.get('quantity', 1)
        
        cart = Cart(request)
        cart.add(room=room, check_in=check_in, check_out=check_out, quantity=quantity, is_room=True)
    return redirect('bookings:cart_detail')

def food_add_to_cart(request, food_id):
    menu_item = get_object_or_404(MenuItem, id=food_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        cart = Cart(request)
        cart.add(menu_item=menu_item, quantity=quantity, is_room=False)
    return redirect('bookings:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart.cart,
        'rooms_total': cart.get_rooms_total(),
        'menu_total': cart.get_menu_total(),
        'grand_total': cart.get_grand_total(),
    }
    return render(request, 'bookings/cart_detail.html', context)

def cart_remove(request, item_id):
    cart = Cart(request)
    is_room = request.GET.get('is_room') == 'true'
    cart.remove(item_id, is_room=is_room)
    return redirect('bookings:cart_detail')

def checkout_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            paid=True
        )
        cart.clear()
        return redirect('bookings:checkout_success')
        
    context = {
        'cart': cart.cart,
        'rooms_total': cart.get_rooms_total(),
        'menu_total': cart.get_menu_total(),
        'grand_total': cart.get_grand_total(),
    }
    return render(request, 'bookings/checkout.html', context)

def checkout_success(request):
    return render(request, 'bookings/checkout_success.html')