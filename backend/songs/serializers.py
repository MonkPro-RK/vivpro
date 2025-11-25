from rest_framework import serializers
from .models import Playlist, SongRating
from users.serializers import UserRegisterSerializer


class SongsRatingSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(read_only=True)
    class Meta:
        model = SongRating
        fields = "__all__"
        


class PlaylistSerializer(serializers.ModelSerializer):
    ratings = SongsRatingSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = "__all__"
