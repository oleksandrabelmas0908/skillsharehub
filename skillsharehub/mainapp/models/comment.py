from django.db import models


class Comment(models.Model):    
    content = models.TextField()
    author = models.ForeignKey('mainapp.CustomUser', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('mainapp.Post', related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.email} at {self.created_at}'