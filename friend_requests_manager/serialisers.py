from rest_framework.serializers import ModelSerializer
from .models import FriendRequest

class DisplayPendingFriendRequestSerialiser(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["from_user"]


class DisplayFriendRequestSerialiser(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["to_user"]

class ManageFriendRequestSerialiser(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["from_user", "to_user"]

    # def create(self, validated_data):
    #     # Create and return a new instance of FriendRequest using the validated data
    #     return FriendRequest.objects.create(**validated_data)    