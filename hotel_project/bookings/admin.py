from django.contrib import admin
from .models import FoodCategory, Room, MenuItem, Booking, Order, OrderItem


from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'paid')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'room', 'check_in', 'check_out', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('check_in', 'created_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

