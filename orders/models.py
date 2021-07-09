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
    order_status = models.ForeignKey('OrderStatus', on_delete=models.PROTECT)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order       = models.ForeignKey('Order', on_delete=models.CASCADE)
    option      = models.ForeignKey('products.Option', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    item_status = models.ForeignKey('ItemStatus', on_delete=models.PROTECT)

    class Meta:
        db_table = 'order_items'

class ItemStatus(models.Model):
    status_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'item_status'

class OrderStatus(models.Model):
    status_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_status'
