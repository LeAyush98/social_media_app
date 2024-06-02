from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserCreationManagerSerialiser(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {'password': {'write_only': True}}  # Hide password field in response

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"].split("@")[0]
        user = User.objects.create_user(**validated_data)  # Create user with hashed password
        return user


class UserDisplaySerialiser(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']