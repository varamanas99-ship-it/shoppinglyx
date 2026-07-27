from django.contrib import admin
from .models import (
    Customer,
    Product,
    ProductImage,  
    Cart,
    OrderPlaced,
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    readonly_fields = ['user']


# ==================== 🆕 MULTIPLE IMAGES INLINE ==================== #
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']
    inlines = [ProductImageInline]  


@admin.register(Cart) 
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity'] 
    readonly_fields = ['user', 'product', 'quantity']
    raw_id_fields = ['user', 'product']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']  
    
    # Aa read-only fields thi dropdown ane badha buttons gayab thai jashe
    readonly_fields = ['user', 'customer', 'product', 'quantity', 'ordered_date']
    raw_id_fields = ['user', 'customer', 'product']