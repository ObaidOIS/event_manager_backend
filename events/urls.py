from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include


urlpatterns =  [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register),
    path('user/', get_users),
    path('events/', get_events),
    path('events/create/', create_event),
    path('events/<int:pk>/', get_event),
    path('events/<int:pk>/update/', update_event),
    path('events/<int:pk>/delete/', delete_event),
    path('events/<int:pk>/invite/', invite_user),
    path('events/<int:pk>/get_invited_users/', get_invited_users),
]
