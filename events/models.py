from django.db import models

class ProductEvent(models.Model):
    image_url  = models.URLField(max_length=500)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_events'

class CategoryEvent(models.Model):
    image_url   = models.URLField(max_length=500)
    category    = models.ForeignKey('products.Category', on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category_events'

class SloganEvent(models.Model):
    image_url  = models.URLField(max_length=500)
    slogan     = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'slogan_events'

class CompanyEvent(models.Model):
    image_url = models.URLField(max_length=500)
    description = models.TextField()
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_events'
