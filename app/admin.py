from django.contrib import admin
from django import forms
from .models import Customer, Product, ProductImage, Cart, OrderPlaced

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        brand = cleaned_data.get("brand")

        # કેટેગરી મુજબની સાચી બ્રાન્ડ્સની યાદી
        mobile_brands = ['iphone', 'Samsung', 'GooglePixel']
        laptop_brands = ['Apple', 'Hp', 'Dell']
        topwear_brands = ['Lee', 'Wrangler', 'Raymond']
        bottomwear_brands = ['Lee', 'Wrangler', 'Spykar']

        # વેલિડેશન ચેક (ખોટી બ્રાન્ડ હશે તો સેવ નહીં થવા દે અને એરર આપશે)
        if category == 'M' and brand and str(brand) not in mobile_brands:
            raise forms.ValidationError("મોબાઈલ કેટેગરી માટે માત્ર મોબાઈલ બ્રાન્ડ (iphone, Samsung, GooglePixel) જ પસંદ કરો!")
        elif category == 'L' and brand and str(brand) not in laptop_brands:
            raise forms.ValidationError("લેપટોપ કેટેગરી માટે માત્ર લેપટોપ બ્રાન્ડ (Apple, Hp, Dell) જ પસંદ કરો!")
        elif category == 'TW' and brand and str(brand) not in topwear_brands:
            raise forms.ValidationError("ટૉપવેર કેટેગરી માટે યોગ્ય બ્રાન્ડ પસંદ કરો!")
        elif category == 'BW' and brand and str(brand) not in bottomwear_brands:
            raise forms.ValidationError("બૉટમવેર કેટેગરી માટે યોગ્ય બ્રાન્ડ પસંદ કરો!")
            
        return cleaned_data


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    readonly_fields = ['user']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    form = ProductAdminForm  
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