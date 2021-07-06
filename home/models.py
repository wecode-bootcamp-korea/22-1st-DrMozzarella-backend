from django.db import models

class ProductEvent(models.Model):
    image_url  = models.URLField()
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
    class Meta:
        db_table = 'product_events'

class CategoryEvent(models.Model):
    image_url = models.URLField()
    category  = models.ForeignKey('products.Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_events'

