from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HelloSerializer, UserProfileSerializer,ProfileFeedItemSerializer
from rest_framework import status
from rest_framework import viewsets
from testAPI import models
from rest_framework.authentication import TokenAuthentication
from testAPI import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly # you can also use IsAuthenticated if you don't want to allow anonymous see it


class HelloAPIView(APIView):
    
    serializer_class = HelloSerializer
    
    def get(self,request):
        res = {"name": "Hello World", "message": "Hello World", "status": "success"}
        hello = self.serializer_class(res)

        return Response(hello.data)
    
    def post(self,request):
        
        hello = self.serializer_class(data=request.data)
        if hello.is_valid():
            x = hello.validated_data.get('message')
            msg = f"hello {x}"
            
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            return Response(hello.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})


    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})
 
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,) #in searchFilter the params is just search like this ?search=hasanPortfolio
    search_fields = ('name', 'email',)
 
    
class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
   

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
                          permissions.UpdateOwnFeed,
                          IsAuthenticatedOrReadOnly,
                          )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)