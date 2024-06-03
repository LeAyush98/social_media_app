from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest
from .serialisers import ManageFriendRequestSerialiser, DisplayFriendRequestSerialiser, DisplayPendingFriendRequestSerialiser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.cache import cache

class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Send a friend request from one user to another.
        Users can not send more than 3 friend requests within a minute.
        """
        serializer = ManageFriendRequestSerialiser(data=request.data)

        if serializer.is_valid():
            from_user = request.data["from_user"]
            to_user = request.data["to_user"]
            

            # Ensure both users exist
            get_object_or_404(User, email=from_user)
            get_object_or_404(User, email=to_user)
             
            # Ensure both users are not same
            if from_user == to_user:
                return Response("You cannot send a request back to yourself", status.HTTP_409_CONFLICT)

            # To make sure that in case if someone rejects a request by mistake, can send the request again
            pre_exisiting_request_check = FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status = "Pending").first()


            if pre_exisiting_request_check:
                return Response("You already have a pending request for this person", status.HTTP_409_CONFLICT)

            # If either of the person has already accepted the friend request then they are friends already    
            already_friends_check = FriendRequest.objects.filter(from_user__in = [from_user, to_user], to_user__in = [to_user, from_user], status = "Accepted").first()
            
            if already_friends_check:
                return Response("You are friend already with this person", status.HTTP_200_OK)

            # Check the rate limit
            cache_key = f"friend_request_{from_user}"
            request_count = cache.get(cache_key, 0)

            if request_count >= 3:
                return Response(
                    {"error": "You have exceeded the limit of 3 friend requests per minute"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # Save the friend request

            friend_request = FriendRequest(from_user = from_user, to_user = to_user)
            friend_request.save()

            # Update the request count in cache
            cache.set(cache_key, request_count + 1, timeout=60)

            return Response("Friend Request Sent", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Accept a friend request.
        """
        serializer = ManageFriendRequestSerialiser(data=request.data)

        if serializer.is_valid():
            from_user = request.data["from_user"]
            to_user = request.data["to_user"]

            # Ensure both users exist
            get_object_or_404(User, email=from_user)
            get_object_or_404(User, email=to_user)

            # Find the specific friend request
            friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=to_user)
         
            # Update the status to Accepted
            friend_request.status = "Accepted"
            friend_request.save()

            # Accepting friend request from friend A to friend B means if there is a pending request from B to A, it is also accepted
            back_to_friend_request = FriendRequest.objects.filter(from_user = to_user, to_user = from_user).first()

            if back_to_friend_request:
         
                # Update the status to Accepted
                back_to_friend_request.status = "Accepted"
                back_to_friend_request.save()

            return Response("Friend Request Accepted", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Reject a friend request.
        """
        serializer = ManageFriendRequestSerialiser(data=request.data)

        if serializer.is_valid():
            from_user = request.data["from_user"]
            to_user = request.data["to_user"]

            # Ensure both users exist
            get_object_or_404(User, email=from_user)
            get_object_or_404(User, email=to_user)

            # Find the specific friend request
            friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=to_user)
            friend_request.delete()

            return Response({"msg": "Friend Request Rejected"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisplayFriends(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Display a list of friends for a user based on accepted friend requests.
        """
        email = request.query_params.get('email')

        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists
        user = get_object_or_404(User, email=email)

        # Find all accepted friend requests for the given email
        friends = FriendRequest.objects.filter(from_user=email, status="Accepted")
        if not friends:
            friends = FriendRequest.objects.filter(to_user=email, status="Accepted")

        # Serialize the data
        serializer = DisplayFriendRequestSerialiser(friends, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class DisplayPendingFriendRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Display a list of pending friend requests received by the user.
        """
        email = request.query_params.get('email')

        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists
        user = get_object_or_404(User, email=email)

        # Find all pending friend requests for the given email
        pending_requests = FriendRequest.objects.filter(to_user=email, status="Pending").all()

        # Serialize the data
        serializer = DisplayPendingFriendRequestSerialiser(pending_requests, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
