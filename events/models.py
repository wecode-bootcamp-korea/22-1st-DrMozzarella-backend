from django.db import models

class ProductEvent(models.Model):
    image_url  = models.URLField()
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_events'

class CategoryEvent(models.Model):
    image_url   = models.URLField()
    category    = models.ForeignKey('products.Category', on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category_events'
