from django.db                import models
from django.dispatch             import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models         import Avg

class Comment(models.Model):
    account    = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True)
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
    account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    flag    = models.BooleanField()

    class Meta:
        db_table = 'comment_likes'

@receiver(post_save, sender=Comment)
def comment_post_save_handler(sender, instance, **kwargs):
    instance.product.score = instance.product.comment_set.aggregate(Avg('score'))["score__avg"]
    instance.save()

@receiver(pre_delete, sender=Comment)
def comment_pre_delete_handler(sender, instance, **kwargs):
    instance.product.score = instance.product.comment_set.aggreage(Avg('score'))["score__avg"]
    instance.save()

@receiver(post_save, sender=CommentLike)
def commentlike_post_save_handler(sender, instance, **kwargs):
    if instance.flag:
        instance.comment.like += 1
    else:
        instance.comment.dislike += 1
    instance.comment.save()

@receiver(pre_delete, sender=CommentLike)
def commentlike_pre_delete_handler(sender, instance, **kwargs):
    if instance.flag:
        instance.comment.like -= 1
    else:
        instance.comment.dislike -= 1
    instance.comment.save()
