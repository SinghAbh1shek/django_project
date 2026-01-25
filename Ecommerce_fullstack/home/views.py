from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import *
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
#  NOTE: to user TrigamSimilarity we must run "CREATE EXTENSION pg_trgm;" query in our pgadmin
from django.db.models import Q
from orders.models import Cart, Wishlist
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from products.documents import VendorProductDocument

@cache_page(60 * 3)
def index(request):

    categories = Category.objects.annotate(
        product_count=Count('cat_child__products', distinct=True)).filter(product_count__gt = 0).order_by("-id")[:10]
    
    

    new_arrivals = ( VendorProduct.objects.filter(product__images__isnull=False)
    .order_by('-created_at').distinct()[:5]
    )

    trending = (VendorProduct.objects.filter(product__images__isnull=False)
    .order_by('-product__trending_score').distinct()[:5]
    )

    top_rated = (VendorProduct.objects.filter(product__images__isnull=False)
    .order_by('-product__product_rating').distinct()[:5]
    )

    new_products = (VendorProduct.objects.filter(product__images__isnull = False)
                   .order_by('-created_at').distinct()[:12])
    
    dropdown_categories = (Category.objects.filter(parent__isnull = True).distinct())

    gaming = Category.objects.filter(parent__category_name__iexact="Gaming")   

    mobile_accessories = Category.objects.filter(parent__category_name__iexact="Mobile Accessories")   
    mobile_accessories = Category.objects.filter(parent__category_name__iexact="Mobile Accessories")   

    

    context = {
        'categories': categories,
        'new_arrivals': new_arrivals,
        'trending': trending,
        'top_rated': top_rated,
        'new_products': new_products,
        'dropdown_categories': dropdown_categories,
        'gaming': gaming,
        'mobile_accessories': mobile_accessories,
        }

    return render(request, 'home.html', context)


def search(request):
    search = request.GET.get('q')



    if search:
        result = VendorProductDocument.search().query(
            'match', product__title = search
        )
        result = result.execute()
        for hit in result:
            print(hit.meta.id)
        products = [
            {
                'id': hit.meta.id,
                'title': hit.product.title,
                'description': hit.product.description,
                'category': hit.product.category,
                'vendor_selling_price': hit.vendor_selling_price,
                'image': hit.product.image_url,
                'mrp': hit.product.mrp,
            } for hit in result
        ]
    else:
        products = None

    # print(search)
    return render(request, 'search.html', context={'products':products})

def product_details(request, id): 
    cache_key = f"product_{id}"

    product = cache.get(cache_key)
    if not product:
        product = VendorProduct.objects.get(id=id)
        cache.set(cache_key, product, 60 * 3)
    
    # product = VendorProduct.objects.get(id=id)

    cart = None
    in_cart = False
    in_wishlist = False

    if request.user.is_authenticated:
        cart = Cart.objects.filter(
            customer=request.user.customer,
            is_paid=False
        ).first()

        wishlist = Wishlist.objects.filter(customer = request.user.customer).first()
        if wishlist:
            in_wishlist = wishlist.has_product(product=product)
        if cart:
            in_cart = cart.has_product(product)

    return render(request, "product_details.html", {
        "product": product,
        "cart": cart,
        "in_cart": in_cart,
        'in_wishlist': in_wishlist,
    })



def categories(request, id):
    def get_all_category_ids_by_id(category_id):
        ids = [category_id]
        children = Category.objects.filter(parent_id=category_id).values_list("id", flat=True)
        for child_id in children:
            ids.extend(get_all_category_ids_by_id(child_id))
        return ids


    category_ids = get_all_category_ids_by_id(id)

    products = VendorProduct.objects.filter(
        product__category_id__in=category_ids, is_active = True
    )[:28]

    categories = Category.objects.annotate(
        product_count=Count('products', distinct=True)).filter(id__in = category_ids, product_count__gt = 0).order_by("-id")[:10]
    
    
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'category.html', context)