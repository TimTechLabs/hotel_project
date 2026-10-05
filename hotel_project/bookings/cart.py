from datetime import datetime

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {'rooms': {}, 'menu_items': {}}
        self.cart = cart

    def add(self, room=None, menu_item=None, check_in=None, check_out=None, quantity=1, is_room=True):
        if is_room and room:
            room_id = str(room.id)
            try:
                ci = datetime.strptime(str(check_in), '%Y-%m-%d').date()
                co = datetime.strptime(str(check_out), '%Y-%m-%d').date()
                nights = (co - ci).days
                if nights <= 0:
                    nights = 1
            except (ValueError, TypeError):
                nights = 1
                ci = check_in
                co = check_out

            qty = int(quantity) if quantity else 1

            self.cart['rooms'][room_id] = {
                'room_id': room.id,
                'name': room.name,
                'price': float(room.price),
                'check_in': str(ci),
                'check_out': str(co),
                'nights': nights,
                'quantity': qty,
                'total_price': float(room.price * nights * qty)
            }
        elif not is_room and menu_item:
            item_id = str(menu_item.id)
            qty = int(quantity) if quantity else 1
            
            if item_id in self.cart['menu_items']:
                self.cart['menu_items'][item_id]['quantity'] += qty
                self.cart['menu_items'][item_id]['total_price'] = float(
                    self.cart['menu_items'][item_id]['quantity'] * menu_item.price
                )
            else:
                self.cart['menu_items'][item_id] = {
                    'item_id': menu_item.id,
                    'name': menu_item.name,
                    'price': float(menu_item.price),
                    'quantity': qty,
                    'total_price': float(menu_item.price * qty)
                }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_id, is_room=True):
        key = str(item_id)
        if is_room:
            if key in self.cart['rooms']:
                del self.cart['rooms'][key]
                self.save()
        else:
            if key in self.cart['menu_items']:
                del self.cart['menu_items'][key]
                self.save()

    def clear(self):
        self.session['cart'] = {'rooms': {}, 'menu_items': {}}
        self.save()

    def get_rooms_total(self):
        return sum(item['total_price'] for item in self.cart.get('rooms', {}).values())

    def get_menu_total(self):
        return sum(item['total_price'] for item in self.cart.get('menu_items', {}).values())

    def get_grand_total(self):
        return self.get_rooms_total() + self.get_menu_total()