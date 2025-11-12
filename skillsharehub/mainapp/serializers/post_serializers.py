from rest_framework import serializers


from skillsharehub.mainapp.models import Post
from .chanel_serializers import ChanelOutSerializer
from .comment_serializers import CommentOutSerializer


class PostOutSerializer(serializers.ModelSerializer):
    chanel_name = serializers.CharField(source='chanel.name', read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "video_link", "description", "created_at", "chanel_name")


class PostDetailSerializer(serializers.ModelSerializer):
    chanel = ChanelOutSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "video_link", "description", "chanel", "comments", "created_at")

    def get_comments(self, obj):
        qs = obj.comments.order_by('-created_at')[:10]
        return CommentOutSerializer(qs, many=True).data

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "video_link", "description", "chanel")
        required_fields = ("title", "video_link", "chanel")

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "video_link", "description")

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.video_link = validated_data.get('video_link', instance.video_link)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

