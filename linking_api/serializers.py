from rest_framework import serializers

from .models import User, Link


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        validated_data["is_active"] = True
        user = User.objects.create_user(**validated_data)
        return user


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "id",
            "usuario",
            "url",
            "description",
        )