from django.db import models
from news.models import News
from django.contrib.auth.models import User
# from notifications.models import Notification
# from properties.models import Post

from django.db.models.signals import post_save, post_delete


# Create your models here.

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        news = comment.news
        text_preview = comment.body[:90]
        #post = Post.objects.all()
        # notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        # notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        # notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
        # notify.delete()


# Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)
