from django.db import models

class Cart(models.Model):
    account    = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    option     = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    quantity   = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'carts'

class Order(models.Model):
    account      = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True)
    ordered_at   = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=36)
    status       = models.ForeignKey('OrderStatus', on_delete=models.PROTECT)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status   = models.ForeignKey('ItemStatus', on_delete=models.PROTECT)

    class Meta:
        db_table = 'order_items'

class ItemStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'item_status'

class OrderStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_status'

class Coupon(models.Model):
    code             = models.CharField(max_length=10)
    expiry_date      = models.DateField(auto_now_add=False)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2)
    discount_price   = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'coupons'
    
