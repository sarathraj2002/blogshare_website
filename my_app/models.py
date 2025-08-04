from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=15)
    profile_pic=models.ImageField(upload_to='profiles/',default='')

class BlogPost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    title=models.CharField(max_length=200)
    content=models.TextField()
    image=models.ImageField(upload_to='posts/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='comments')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


