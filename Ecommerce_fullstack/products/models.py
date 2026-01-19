from django.db import models
from utils.utility.models import BaseModel
from accounts.models import Shopkeeper

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='cat_child', null=True, blank=True)

    def __str__(self):
        return self.category_name
    
    def is_leaf(self):
        return not self.cat_child.exists()

    def get_first_product_image(self):

        if self.is_leaf():
            product = self.products.first()
            if product and product.images.first():
                return product.images.first().image.url
            return None

        for child in self.cat_child.all():
            image = child.get_first_product_image()
            if image:
                return image

        return None


class Product(BaseModel):
    title = models.CharField(max_length=225)
    highlight = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    product_rating = models.FloatField(null=True, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)

    trending_score = models.FloatField(default=0)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.title

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

class VendorProduct(BaseModel):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_products')
    vendor_rating = models.FloatField(null=True, blank=True)
    vendor_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('shopkeeper', 'product')

    def get_first_image(self):
        image =  self.product.images.first().image.url
        if image:
            return f"http://127.0.0.1:8000{image}"
        else:
            return None

    def __str__(self):
        return f"{self.shopkeeper} - {self.product}"


