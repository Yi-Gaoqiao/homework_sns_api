from rest_framework import serializers
from core.models import Post
from api_user.serializers import ProfileSerializer

class PostSerializer(serializers.ModelSerializer):
    """Serializer for post model"""

    postBy = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'postBy', 'content', 'posted_at')
        # extra_kwargs = {'postBy': {'read_only': True}}
        read_only_fields = ('postBy', 'posted_at',)