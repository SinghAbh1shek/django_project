from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Cart, CartItems, Wishlist, Order, OrderItems
from accounts.models import Customer
from products.models import VendorProduct
from django.contrib.auth.decorators import login_required
from .payments import RazorPayPayment
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from utils.utility.utility import generate_order_pdf

@login_required(login_url='login')
def get_cart(request):
    cart = None
    try:    
        cart = Cart.objects.get(customer = request.user.customer, is_paid = False)

    except Exception as e:
        print(e)
        print("Something Wrong")
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout_view(request):
    cart = None
    payment_info = {}
    amount = 0
    try:
        cart = Cart.objects.get(
            customer=request.user.customer,
            is_paid=False
        )
        amount = float(cart.getCartTotal())
        receipt = request.user.username


        callback_url = request.build_absolute_uri(reverse("success"))

        payment = RazorPayPayment('INR')
        payment_info = payment.process_payment(amount * 100, receipt)
        cart.order_id = payment_info['id']
        cart.save()
            
    except Exception as e:
        print('Something Goes Wrong')
        return redirect('cart')

    context = {
        "cart": cart,
        "payment_info": payment_info,
        "amount": int(amount * 100),
        "callback_url": callback_url,
    }
    return render(request, "checkout.html", context)

@csrf_exempt
def success(request):
    if request.method != "POST":
        return redirect("cart") 
    try:
        razorpay_payment_id  = request.POST.get('razorpay_payment_id')
        razorpay_order_id  = request.POST.get('razorpay_order_id')
        razorpay_signature  = request.POST.get('razorpay_signature')

        cart = Cart.objects.get(order_id = razorpay_order_id)
        cart.is_paid = True
        cart.payment_id = razorpay_payment_id
        cart.payment_signature = razorpay_signature
        cart.convert_to_order()
        cart.save()

        return render(request, 'success.html')
    except Exception as e:
        print('Something Wrong')
        print(e)
        return redirect('home')


@login_required(login_url='login')
def add_to_cart(request):
    try:
        user = request.user.id
        product = request.GET.get('product_id')
        customer = Customer.objects.get(user  = user)
        product = VendorProduct.objects.get(id = product)
        cart, _ = Cart.objects.get_or_create(customer = customer, is_paid = False)
        cart_item, _ = CartItems.objects.get_or_create(cart = cart, product = product)
        cart_item.quantity += 1
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print('Something is wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_to_cart(request):
    try:
        user = request.user.id
        customer = Customer.objects.get(user = user)
        product_id = request.GET.get('product_id')
        product = VendorProduct.objects.get(id = product_id)
        cart = Cart.objects.get(customer = customer, is_paid = False)
        cart_item = CartItems.objects.filter(cart = cart, product=product)
        if cart_item.exists():
            cart_item = cart_item[0]
            cart_item.quantity -= 1

            if cart_item.quantity <=0:
                cart_item.delete()
            else:
                cart_item.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        print(e)
        print('Something is wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_item_from_cart(request):
    try:
        product_id = request.GET.get("product_id")
        product = VendorProduct.objects.get(id = product_id)
        cart = Cart.objects.get(customer = request.user.customer, is_paid=False)
        cart_items = CartItems.objects.filter(cart = cart, product = product)
        if cart_items.exists():
            cart_items.delete()
            cart_items.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

    except Exception as e:
        print('Something goes wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def empty_cart(request):
    try:
        cart = Cart.objects.get(customer = request.user.customer, is_paid=False)
        cart.clear_cart()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        print('Something goes wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def add_to_wishlist(request):
    product_id = request.GET.get('product_id')
    product = VendorProduct.objects.get(id = product_id)
    wishlist, _ = Wishlist.objects.get_or_create(customer = request.user.customer)
    wishlist.add_product(product = product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_to_wishlist(request):
    product_id = request.GET.get('product_id')
    product = VendorProduct.objects.get(id = product_id)
    wishlist = Wishlist.objects.get(customer = request.user.customer)
    wishlist.remove_product(product = product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def wishlist(request):
    wishlists = None
    try:
        wishlists = Wishlist.objects.get(customer = request.user.customer)
    except Exception as e:
        print("Something  goes wrong")
    context = {
        'wishlists': wishlists
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='login')
def moves_to_wishlist(request):
    try:
        customer = request.user.customer
        product_id = request.GET.get("product_id")
        product = VendorProduct.objects.get(id = product_id)
        wishlist = Wishlist.objects.get(customer = customer)
        cart = Cart.objects.get(customer = customer, is_paid=False)
        cart_items = CartItems.objects.filter(cart = cart, product = product)
        wishlist.add_product(product=product)
        if cart_items.exists():
            cart_items.delete()
            cart_items.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

    except Exception as e:
        print(e)
        print('Something goes wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(customer = request.user.customer).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'order.html', context)

@login_required(login_url='login')
def order_details(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id = order_id)
    order_items = OrderItems.objects.filter(order = order)
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'order_details.html', context)

@login_required(login_url='login')
def generate_invoice(request):
    try:
        id = request.GET.get('id')
        order = Order.objects.get(id = id)
        if not order.invoice_pdf:
            generate_order_pdf(order, order.get_order_data())

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print('Something Goes Wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
