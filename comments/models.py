from django.db import models

class Comment(models.Model):
    account    = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    review     = models.TextField()
    score      = models.DecimalField(max_digits=2, decimal_places=1)
    like       = models.IntegerField()
    dislike    = models.IntegerField()
    title      = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

class CommentLike(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    flag    = models.BooleanField()

    class Meta:
        db_table = 'comment_likes'
