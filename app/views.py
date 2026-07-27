from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Customer, Product, ProductImage, Cart, OrderPlaced, CustomerReview
from .forms import CustomerRegistrationForm, LoginForm, MyPasswordChangeForm, CustomerProfileForm 
from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView 
from django.urls import reverse_lazy 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.db.models import Q


class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        fashion = topwears | bottomwears 
        
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()

        return render(request, 'app/home.html', {
            'mobiles': mobiles,
            'laptops': laptops,
            'fashion': fashion,
            'totalitem': totalitem,
        })


class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            
        return render(request, 'app/productdetail.html', {
            'product': product, 
            'totalitem': totalitem
        })


class customerRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
        
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
            
        form = CustomerRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            messages.success(request, 'Congratulations!! Registered Successfully')
            return redirect('home') 
            
        return render(request, 'app/customerregistration.html', {'form': form})


class CustomerLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    # Admin login thay etle seedho admin panel par redirect karva mate
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return '/admin/'
        return reverse_lazy('home')


class CustomerLogoutView(LogoutView):
    next_page = 'login'  


class CustomerPasswordChangeView(PasswordChangeView):
    template_name = 'app/changepassword.html'
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('passwordchangedone')


@login_required
def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()

    if 'laptop' in request.path:
        if data is None:
            laptops = Product.objects.filter(category='L')
        else:
            laptops = Product.objects.filter(category='L', brand=data)
            
        return render(request, 'app/mobile.html', { 
            'mobile': laptops,
            'totalitem': totalitem
        })
    else:
        if data is None:
            mobiles = Product.objects.filter(category='M')
        else:
            mobiles = Product.objects.filter(category='M', brand=data)
            
        return render(request, 'app/mobile.html', {
            'mobile': mobiles, 
            'totalitem': totalitem
        })


@login_required
def topwear(request, data=None):
    if data is None:
        topwears = Product.objects.filter(category='TW')
    else:
        topwears = Product.objects.filter(category='TW', brand=data)
        
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        
    return render(request, 'app/topwear.html', {
        'topwear': topwears, 
        'totalitem': totalitem
    })


@login_required
def bottomwear(request, data=None):
    if data is None:
        bottomwears = Product.objects.filter(category='BW')
    else:
        bottomwears = Product.objects.filter(category='BW', brand=data)
        
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        
    return render(request, 'app/bottomwear.html', {
        'bottomwear': bottomwears, 
        'totalitem': totalitem
    })


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    if product_id:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('showcart')
    return redirect('showcart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        totalitem = Cart.objects.filter(user=user).count()
        cart_product = [p for p in Cart.objects.filter(user=user)]
        
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {
                'carts': cart, 
                'totalamount': totalamount, 
                'amount': amount,
                'totalitem': totalitem
            })
        else:
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        for p in cart_product:
            amount += (p.quantity * p.product.discounted_price)
        
        product_total = c.quantity * c.product.discounted_price

        data = {
            'quantity': c.quantity, 
            'amount': amount, 
            'totalamount': amount + shipping_amount,
            'product_total': product_total
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        for p in cart_product:
            amount += (p.quantity * p.product.discounted_price)
        
        product_total = c.quantity * c.product.discounted_price

        data = {
            'quantity': c.quantity, 
            'amount': amount, 
            'totalamount': amount + shipping_amount,
            'product_total': product_total
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        for p in cart_product:
            amount += (p.quantity * p.product.discounted_price)
        data = {
            'amount': amount, 
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


@login_required
def buy_now(request):
    product_id = request.GET.get('prod_id')
    if product_id:
        return redirect(f'/checkout/?prod_id={product_id}')
    return redirect('home')


@login_required
def profile(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
            return redirect('address')
    else:
        form = CustomerProfileForm()
    return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def edit_address(request, id):
    addr = Customer.objects.get(pk=id, user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address Updated Successfully!!')
            return redirect('address')
    else:
        form = CustomerProfileForm(instance=addr)
    return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def delete_address(request, id):
    addr = Customer.objects.get(pk=id, user=request.user)
    addr.delete()
    messages.success(request, 'Address Deleted Successfully!!')
    return redirect('address')


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return render(request, 'app/orders.html', {'order_placed': op, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=user).count()
        
    product_id = request.GET.get('prod_id')
    if product_id:
        product = Product.objects.get(id=product_id)
        quantity = 1  # Buy now mate default quantity 1
        amount = product.discounted_price * quantity
        return render(request, 'app/checkout.html', {
            'add': add, 
            'product': product, 
            'quantity': quantity,
            'totalamount': amount + 70.0, 
            'totalitem': totalitem
        })
    else:
        cart_items = Cart.objects.filter(user=user)
        if not cart_items: 
            return redirect('showcart')
        amount = 0.0
        for p in cart_items: 
            amount += (p.quantity * p.product.discounted_price)
        return render(request, 'app/checkout.html', {
            'add': add, 
            'cart_items': cart_items, 
            'totalamount': amount + 70.0, 
            'totalitem': totalitem
        })


@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('custid')
    product_id = request.GET.get('prodid') 
    if not cust_id:
        messages.warning(request, "Please add or select a delivery address first!")
        return redirect('checkout')
    try:
        customer = Customer.objects.get(id=cust_id)
    except Customer.DoesNotExist:
        return redirect('checkout')
    if product_id:
        product = Product.objects.get(id=product_id)
        OrderPlaced(user=user, customer=customer, product=product, quantity=1, status='Pending').save()
    else:
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, status='Pending').save()
            c.delete() 
    messages.success(request, "Congratulations!! Your Order Placed Successfully")
    return redirect("orders")


@login_required
def cancel_order(request, id):
    order = OrderPlaced.objects.get(pk=id, user=request.user)
    order.delete()
    messages.success(request, 'Order Cancelled Successfully!!')
    return redirect('orders')


def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return render(request, 'app/about.html', {'totalitem': totalitem})


def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return render(request, 'app/contact.html', {'totalitem': totalitem})


def review(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if comment:
            CustomerReview.objects.create(user=request.user, rating=int(rating), comment=comment)
            return redirect('review')
    all_reviews = CustomerReview.objects.all().order_by('-created_at')
    return render(request, 'app/review.html', {'totalitem': totalitem, 'reviews': all_reviews})


@login_required
def delete_review(request, id):
    review = get_object_or_404(CustomerReview, pk=id, user=request.user)
    review.delete()
    messages.success(request, 'તમારો રિવ્યુ ડીલીટ થઈ ગયો છે!')
    return redirect('review')

