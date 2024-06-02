from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .serialisers import UserCreationManagerSerialiser, UserDisplaySerialiser


class UserCreate(APIView):
    """
    API to handle user registration.
    """

    def post(self, request):
        data = request.data

        # Check if required credentials are provided
        if "email" not in data.keys() or "password" not in data.keys():
            return Response({"msg": "Missing Required Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure email is case insensitive
        data["email"] = data["email"].lower()

        # Serialize the data
        serializer = UserCreationManagerSerialiser(data=data)

        # Check if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response("User Registered", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    API to handle user login and provide JWT tokens.
    """
    
    def post(self, request):
        data = request.data

        # Check if required credentials are provided
        if "email" not in data.keys() or "password" not in data.keys():
            return Response({"msg": "Missing Required Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = data.get("email").lower()
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # User with the given email doesn't exist
            user = None

        # Check if the user exists and if the password matches the hashed password
        if user is not None and check_password(password, user.password):

        # If user is authenticated, generate and return JWT tokens
        
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        # If authentication fails, return an error response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserSearch(APIView):
    """
    API to search users by email or name.
    Supports pagination up to 10 records per page.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_keyword = request.query_params.get('search', '')

        # Check if search keyword is provided
        if not search_keyword:
            return Response({"error": "Search keyword is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search by exact email match or partial name match
        if '@' in search_keyword:
            users = User.objects.filter(email__iexact=search_keyword)
        else:
            users = User.objects.filter(
                Q(first_name__icontains=search_keyword) |
                Q(last_name__icontains=search_keyword) |
                Q(username__icontains=search_keyword)
            )

        # Paginate the results
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)

        # Serialize the paginated results
        serializer = UserDisplaySerialiser(result_page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
