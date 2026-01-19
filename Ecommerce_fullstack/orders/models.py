from django.db import models
from accounts.models import Customer
from products.models import VendorProduct
from django.db.models import Sum, F
from utils.utility.models import BaseModel
from utils.utility.utility import generate_order_id, generate_order_pdf


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_cart')
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=1000, null=True, blank=True)

    def has_product(self, product):
        return self.cart_items.filter(product=product).exists()
    
    def getCartTotal(self):
        total = self.cart_items.aggregate(
            total = Sum(F('product__vendor_selling_price') * F('quantity'))
        )['total']
        return total or 0
    
    def clear_cart(self):
        self.cart_items.all().delete()

    def convert_to_order(self):
        if not Order.objects.filter(cart = self).exists():
            order = Order.objects.create(
                cart = self,
                customer = self.customer,
                payment_id = self.payment_id,
                payment_signature = self.payment_signature,
                total = self.getCartTotal()
            )
            for cart_item in self.cart_items.all():
                OrderItems.objects.create(
                    order = order,
                    product = cart_item.product,
                    quantity = cart_item.quantity,
                    price = cart_item.product.vendor_selling_price
                )
            generate_order_pdf(order, order.get_order_data())

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(VendorProduct, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)

    def getTotalPrice(self):
        return self.quantity * self.product.vendor_selling_price
    
class Wishlist(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')

    def has_product(self, product):
        return self.items.filter(product = product).exists()
    
    def add_product(self, product):
        self.items.get_or_create(product = product)
    
    def remove_product(self, product):
        self.items.filter(product = product).delete()

class WishlistItems(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(VendorProduct, on_delete=models.CASCADE)


class Order(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_order')
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=1000, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.order_id = generate_order_id(str(Order.objects.count()+1))
        super(Order, self).save(*args, **kwargs)

    def get_order_data(self):
        data = {
            'customer':{
                'name': self.customer.user.first_name,
                'phone': self.customer.phone or None,
                'email': self.customer.user.email or None,
            },
            'order': {
                'order_id': self.order_id,
                'total': self.total,
            },
            'order_items': []
        }
        order_items = [
            {
                'product': item.product.product.title,
                'quantity': item.quantity,
                'price': item.price,
                'total_price': item.price * item.quantity,
                'image': item.product.get_first_image(),
            }
            for item in self.order_items.all()
        ]
        data['order_items'] = order_items

        return data

    def __str__(self):
        return self.order_id
    

class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(VendorProduct, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity