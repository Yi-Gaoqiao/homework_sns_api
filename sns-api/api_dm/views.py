from rest_framework import viewsets, authentication, permissions, status
from api_dm import serializers
from core.models import Message
from rest_framework.response import Response

class MessageViewSet(viewsets.ModelViewSet):
    """Handles creating Message"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete DM is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Update DM is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch DM is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class InboxListView(viewsets.ReadOnlyModelViewSet):
    """Check the Message inbox"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)


# class InboxListView(generics.ListAPIView):
#     """Check the Message inbox"""
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.MessageSerializer
#     queryset = Message.objects.all()

#     def get_queryset(self):
#         return self.queryset.filter(receiver=self.request.user)