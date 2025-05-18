"""
URL configuration for the user management app.

This module defines the URL patterns for the user management functionality,
including registration, login, logout, contact us, and password reset API endpoints.

It also sets up a router for ViewSets.

Typical usage example:

    urlpatterns = [
        path('register/', RegistrationAPIView.as_view(), name='register'),
        path('', include(router.urls)),
    ]

"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter  # type: ignore
from rest_framework_simplejwt.views import TokenRefreshView

from user_management.views import (
    ContactUsCreateView,
    LogoutAPIView,
    MyTokenObtainPairView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PreferenceViewSet,
    ProfileViewSet,
    RegistrationAPIView,
    UserLikedRestaurantViewSet,
    UserPreferenceViewSet,
    find_similar_users,
    recommend_restaurants,
)

# Define the router for ViewSets.
router = DefaultRouter()

# Register ProfileViewSet, BookmarkViewset, PreferenceViewSet, UserPreferenceViewSet, and
# UserLikedRestaurantViewSet with the router, to allow curd operations.
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"preferences", PreferenceViewSet)
router.register(r"user-preferences", UserPreferenceViewSet)
router.register(r"user-liked-restaurants", UserLikedRestaurantViewSet)

urlpatterns = [
    # Endpoint for registration.
    path("register/", RegistrationAPIView.as_view(), name="register"),
    # Endpoint for login and token refresh.
    path("login/", MyTokenObtainPairView.as_view(), name="token-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Endpoint for logout.
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    # Endpoint for contact us.
    path("contact-us/", ContactUsCreateView.as_view(), name="contact-us"),
    # Endpoint for password reset.
    path("reset-password/", PasswordResetRequestView.as_view(),
         name="reset-password"),
    # Endpoint for password reset confirmation
    path('reset-password/confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(), name='reset-password-confirm'),


    # Include router URLs.
    path("", include(router.urls)),
    path("users/similar/", find_similar_users, name="find_similar_users"),
    path("restaurants/recommend/", recommend_restaurants,
         name="recommend_restaurants"),
]
