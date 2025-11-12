from rest_framework import serializers
from skillsharehub.mainapp.models import Chanel
from .user_serializers import UserSerializer


class ChanelOutSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    subscriber_count = serializers.IntegerField(source='subscribers.count', read_only=True)

    class Meta:
        model = Chanel
        fields = ("id", "name", "created_at", "owner", "subscriber_count")


class ChanelCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Chanel
        fields = ("name", "owner")

    def create(self, validated_data):
        request = self.context.get('request') if self.context else None
        owner = getattr(request, 'user', None)
        if owner is None or owner.is_anonymous:
            raise serializers.ValidationError({"owner": "Authenticated user required."})
        return Chanel.objects.create(owner=owner, **validated_data)

    def update(self, instance, validated_data):
        # Prevent changing owner via updates
        validated_data.pop('owner', None)
        return super().update(instance, validated_data)


class ChanelDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    subscribers = UserSerializer(many=True, read_only=True)
    publications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Chanel
        fields = ("id", "name", "created_at", "owner", "subscribers", "publications")