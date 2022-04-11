from django.urls import path, include
from .views import HelloAPIView, HelloViewSet, UserProfileViewSet, UserLoginApiView,UserProfileFeedViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, basename='hello-viewset')
router.register('profiles', UserProfileViewSet, basename='profiles')
router.register('feed',UserProfileFeedViewSet, basename='feed')
urlpatterns = [
    path('', include(router.urls)),
    path('hello/', HelloAPIView.as_view(), name='hello_api'),
    path('signin/', UserLoginApiView.as_view(), name='signin'),
]
