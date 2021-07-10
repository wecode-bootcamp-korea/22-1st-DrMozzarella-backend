from django.db                import models
from django.dispatch          import receiver
from django.db.models.signals import post_save
from django.db.models         import Sum

class Product(models.Model):
    name                  = models.CharField(max_length=50)
    summary               = models.TextField()
    description           = models.TextField()
    max_price             = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales                 = models.IntegerField(default=0)
    stocks                = models.IntegerField(default=0)
    score                 = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    thumbnail_image_url   = models.URLField(max_length=500)
    hover_image_url       = models.URLField(max_length=500)
    description_image_url = models.URLField(max_length=500)
    category              = models.ManyToManyField('Category', through='ProductCategory')
    status                = models.BooleanField(default=True)
    nutrition             = models.ForeignKey('Nutrition', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'products'

class ProductCategory(models.Model):
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_categories'

class Category(models.Model):
    menu        = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    image_url   = models.URLField(max_length=500)
    description = models.TextField()

    class Meta:
        db_table = 'categories'

class Menu(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'menus'

class Image(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = 'images'

class Option(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    weight  = models.IntegerField()
    price   = models.DecimalField(max_digits=10, decimal_places=2)
    sales   = models.IntegerField(default=0)
    stocks  = models.IntegerField(default=0)

    class Meta:
        db_table = 'options'

class Nutrition(models.Model):
    calories            = models.IntegerField()
    total_fat           = models.IntegerField()
    saturated_fat       = models.IntegerField()
    trans_fat           = models.IntegerField()
    cholestrol          = models.IntegerField()
    sodium              = models.IntegerField()
    total_carbohydrates = models.IntegerField()
    dietary_fiber       = models.IntegerField()
    sugars              = models.IntegerField()
    protein             = models.IntegerField()
    vitamin_a           = models.IntegerField()
    vitamin_c           = models.IntegerField()
    calcium             = models.IntegerField()
    iron                = models.IntegerField()

    class Meta:
        db_table = 'nutritions'

@receiver(post_save, sender=Option)
def option_post_save_handler(sender, instance, **kwargs):
    instance.product.max_price = instance.product.option_set.all().order_by('-price').first().price 
    instance.product.sales     = instance.product.option_set.aggregate(Sum('sales'))['sales__sum']
    instance.product.sales     = instance.product.option_set.aggregate(Sum('stocks'))['stocks__sum']
    instance.product.save()
