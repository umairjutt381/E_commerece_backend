from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[("admin", "Admin"), ("customer", "Customer")],
        default="customer"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role)

        if role == "admin":
            user.is_staff = True
            user.save()

        return user
