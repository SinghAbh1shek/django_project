from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import VendorProduct

@registry.register_document
class VendorProductDocument(Document):

    product = fields.ObjectField(properties={
        "title": fields.TextField(),
        "description": fields.TextField(),
        "category": fields.KeywordField(),
        "image_url": fields.KeywordField(),
        "mrp": fields.KeywordField(),
    })
     
    class Index:
        name = 'django-ecomm-vendor-products'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = VendorProduct
        fields = [
            'vendor_selling_price'
        ]
    
    def prepare_product(self, instance):
        product = instance.product
        if not product:
            return {}

        return {
            "title": product.title,
            "description": product.description or "",
            "category": product.category.category_name if product.category else "",
            "image_url": f"http://127.0.0.1:8000/{product.images.first().image.url}",
            "mrp": product.mrp,
        }