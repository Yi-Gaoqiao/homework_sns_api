from rest_framework import serializers
from core.models import User, Profile, FriendRequest, Message
from django.db.models import Q

class FriendFilter(serializers.PrimaryKeyRelatedField):
    """filter for receiver"""

    def get_queryset(self):
        request = self.context['request']
        friends = FriendRequest.objects.filter(Q(requestTo=request.user) & Q(approved=True))

        list_friend = []
        for friend in friends:
            list_friend.append(friend.requestFrom.id)

        queryset = User.objects.filter(id__in=list_friend)
        return queryset


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for message model"""

    receiver = FriendFilter()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message')
        extra_kwargs = {'sender': {'read_only': True}}