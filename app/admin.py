from django.contrib import admin
from django import forms
from .models import Customer, Product, ProductImage, Cart, OrderPlaced

# 1. Admin Form banavo je category mutabik brands filter kare
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # By default badhi brands rakho, baaki tame admin ma data save karso tyare validation thi handle thase
        # Je thi JavaScript vagar direct options manage thay

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    readonly_fields = ['user']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    form = ProductAdminForm  # Ahiya form connect karyo
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'category', 'brand', 'product_image']
    inlines = [ProductImageInline]  
    fields = ['title', 'selling_price', 'discounted_price', 'description', 'category', 'brand', 'product_image']

@admin.register(Cart) 
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity'] 
    readonly_fields = ['user', 'product', 'quantity']
    raw_id_fields = ['user', 'product']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']  
    readonly_fields = ['user', 'customer', 'product', 'quantity', 'ordered_date']
    raw_id_fields = ['user', 'customer', 'product']