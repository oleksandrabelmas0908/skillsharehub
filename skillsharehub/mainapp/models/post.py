from django.db import models



class Post(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comments_list = models.ManyToManyField('mainapp.Comment', related_name='post_comments', blank=True)

    chanel = models.ForeignKey('mainapp.Chanel', related_name='posts', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title