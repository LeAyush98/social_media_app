from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, RejectFriendRequest, DisplayFriends, DisplayPendingFriendRequests

urlpatterns = [
    path("send_friend_request", SendFriendRequest.as_view()),
    path("accept_friend_request", AcceptFriendRequest.as_view()),
    path("reject_friend_request", RejectFriendRequest.as_view()),
    path("display_friends", DisplayFriends.as_view()),
    path("display_pending_requests", DisplayPendingFriendRequests.as_view()),
]