from rest_framework import viewsets, authentication, permissions, pagination, response
from core.models import Post
from api_post import serializers

class PostPermission(permissions.BasePermission):
    """Custom permission for PostViewSet"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.postBy.base_user.id == request.user.id


class PostPagination(pagination.PageNumberPagination):
    """Get 2 Todo items in a page"""
    page_size = 2

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size,
            'range_first': (self.page.number * self.page_size) - (self.page_size) + 1,
            'range_last': min((self.page.number * self.page_size), self.page.paginator.count),
        })


class PostViewSet(viewsets.ModelViewSet):
    """Create post for current logged in user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, PostPermission)
    serializer_class = serializers.PostSerializer
    # add 'order_by' when using pagination
    queryset = Post.objects.order_by('-posted_at')
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(postBy=self.request.user.base_user)