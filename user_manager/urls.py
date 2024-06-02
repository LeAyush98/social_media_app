from django.urls import path
from .views import UserCreate, UserLogin, UserSearch

urlpatterns = [
    path("create_user", UserCreate.as_view()),
    path("login_user", UserLogin.as_view()),
    path("search_user", UserSearch.as_view()),
]