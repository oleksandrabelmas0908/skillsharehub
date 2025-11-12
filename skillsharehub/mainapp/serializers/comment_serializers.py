from rest_framework import serializers

from skillsharehub.mainapp.models import Comment


class CommentOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "post", "author", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    
    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        return self.create(validated_data)