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

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']  
    
    # 🆕 આનાથી ડ્રોપડાઉન અને પેન્સિલ/પ્લસ/આંખના બધા જ બટનો ગાયબ થઈ જશે અને માત્ર રીડ-ઓનલી ટેક્સ્ટ કે આઈડી જ દેખાશે
    readonly_fields = ['user', 'customer', 'product', 'quantity']
    raw_id_fields = ['user', 'customer', 'product']