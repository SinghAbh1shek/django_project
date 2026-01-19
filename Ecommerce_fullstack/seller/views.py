from django.shortcuts import render, redirect
from products.models import VendorProduct, Category, Product
from orders.models import OrderItems
from django.db.models import Sum, F
from products.models import Product
from django.contrib.auth.decorators import login_required
from accounts.models import UserRole, Shopkeeper


@login_required(login_url='login')
def home(request):

    try:

        shopkeeper = request.user.shopkeeper

        total_product = VendorProduct.objects.filter(
            shopkeeper = shopkeeper
        ).count()

        active_product = VendorProduct.objects.filter(
            shopkeeper = shopkeeper, is_active = True
        ).count()

        order_items = OrderItems.objects.filter(
            product__shopkeeper = shopkeeper,
            order__cart__is_paid = True
        )

        total_orders = order_items.values('order').distinct().count()

        total_revenue = order_items.aggregate(
            total = Sum(F('price') * F('quantity'))
        )['total'] or 0

        recent_orders = order_items.select_related(
            'order', 'product'
        ).order_by('-created_at')[:10]
    
    except Exception as e:
        print('Something Goes Wrong')
        return redirect('seller_onboarding')

    context = {
        'total_product': total_product,
        'active_product': active_product,
        'total_orders': total_orders,
        'total_revenue':total_revenue,
        'recent_orders': recent_orders
    }

    return render(request, 'seller_home.html', context)

@login_required(login_url='login')
def seller_add_product(request):
    shopkeeper = request.user.shopkeeper

    categories = Category.objects.filter(cat_child__isnull=True)

    selected_category_id = request.GET.get('category')

    if selected_category_id:
        product_lists = Product.objects.filter(
            category_id=selected_category_id
        )
    else:
        product_lists = Product.objects.none()

    if request.method == "POST":
        product_id = request.POST.get('product')
        price = request.POST.get('price')
        is_active = request.POST.get('is_active') == 'on'


        if product_id and price:
            VendorProduct.objects.get_or_create(
                shopkeeper=shopkeeper,
                product_id=product_id,
                defaults={
                    'vendor_selling_price': price,
                    'is_active': is_active
                }
            )

        return redirect('list_product')

    context = {
        'categories': categories,
        'product_lists': product_lists,
        'selected_category_id': selected_category_id
    }

    return render(request, 'add_product.html', context)


@login_required(login_url='login')
def list_product(request):
    shopkeeper = request.user.shopkeeper
    products = VendorProduct.objects.filter(shopkeeper = shopkeeper)
    print(products)
    context = {
        'products': products
    }
    return render(request, 'list_product.html', context)

@login_required(login_url='login')
def seller_onboarding(request):
    try:
        user = request.user
        user_role = UserRole.objects.get(user=user)
        
        if user_role.is_seller == True:
            return redirect('seller_home')

        if request.method == 'POST':
            shop_name = request.POST.get('shop_name')
            bmp_id = request.POST.get('bmp_id')
            gst_number = request.POST.get('gst_number')
            adhar_number = request.POST.get('adhar_number')
            adhar_image = request.FILES.get('adhar_image')

            if not shop_name or not bmp_id or not gst_number or not adhar_image or not adhar_number:
                print('All fields requires')
                return redirect('seller_onboarding')
            
            if Shopkeeper.objects.filter(adhar_number = adhar_number).exists():
                print('Adhar number already exist')
                return redirect('seller_onboarding')
            
            if Shopkeeper.objects.filter(gst_number = gst_number).exists():
                print('GST number already exist')
                return redirect('seller_onboarding')
            
            if Shopkeeper.objects.filter(bmp_id = adhar_number).exists():
                print('BMP ID already exist')
                return redirect('seller_onboarding')

            shopkeeper, _ = Shopkeeper.objects.get_or_create(user = user)
            shopkeeper.shop_name = shop_name
            shopkeeper.bmp_id = bmp_id
            shopkeeper.gst_number = gst_number
            shopkeeper.adhar_number = adhar_number
            shopkeeper.adhar_image = adhar_image
            shopkeeper.save()

            user_role = UserRole.objects.get(user=user)
            user_role.is_seller = True
            user_role.save()
            
            return redirect('seller_home')
    except Exception as e:
        print(e)
        print('Something Goes Wrong')
        return redirect('seller_onboarding')
    
    return render(request, 'seller_onboarding.html')