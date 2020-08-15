from django.shortcuts import render
from rest_framework import viewsets, generics, authentication, permissions, status
from api_user import serializers
from core.models import Profile, FriendRequest
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class FriendRequestViewSet(viewsets.ModelViewSet):
    """Handles creating Friend Request"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        """Get friend requests that are addressed to its own or to others"""
        return self.queryset.filter(Q(requestTo=self.request.user) | Q(requestFrom=self.request.user))

    def perform_create(self, serializer):
        """set a current logged in user automatically"""
        try:
            serializer.save(requestFrom=self.request.user, approved=False)

        except:
            raise ValidationError("User can have only unique request")

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfilePermission(permissions.BasePermission):
    """Custom permission for ProfileViewSet"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.base_user.id == request.user.id


class ProfileViewSet(viewsets.ModelViewSet):
    """Create profile for current logged in user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ProfilePermission)
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save(base_user=self.request.user)


class MyProfileListView(generics.ListAPIView):
    """Get profile for current logged in user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(base_user=self.request.user)