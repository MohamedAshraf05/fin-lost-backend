from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'item-types', ItemTypeViewSet)
router.register(r'ads', AdViewSet)
router.register(r'chats', ChatMessageViewSet)
router.register(r'interactions', AdInteractionHistoryViewSet)
router.register(r'ratings', UserRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Authentication jwt
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", RegisterView.as_view(), name="register"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
