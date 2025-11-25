
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Playlist, SongRating
from .serializers import PlaylistSerializer, SongsRatingSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PlaylistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    
class PlaylistViewSet(ReadOnlyModelViewSet):
    queryset = Playlist.objects.all().order_by("id")
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PlaylistPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'title',
                openapi.IN_QUERY,
                description="Song title to search",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={200: PlaylistSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=["GET"],
        url_path="by-title",
        pagination_class=None
    )
    def get_by_title(self, request):
        title = request.query_params.get("title", None)

        if not title:
            return Response(
                {"error": "title query param is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        songs = Playlist.objects.filter(title__icontains=title)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
    
      
      
class SongRatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'song_id',
                openapi.IN_QUERY,
                description="Song ID to rate",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'rating',
                openapi.IN_QUERY,
                description="Song rating (0–5)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=None,
        responses={200: SongsRatingSerializer(many=True)}
    )


    @action(
        detail=False,
        methods=["POST"],
        url_path="rate-song",
        pagination_class=None
    )
    def rate_the_song(self, request):

        song_id = request.data.get("song_id")
        user_id = request.data.get("user_id")
        rating = request.data.get("rating")

        if not song_id or not user_id or not rating:
            return Response(
                {"error": "song_id, user_id, rating are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        # Convert rating to int and validate
        try:
            rating = int(rating)
        except ValueError:
            return Response({"error": "rating must be an integer"}, status=400)

        if rating < 0 or rating > 5:
            return Response({"error": "rating must be between 0 and 5"}, status=400)

        # Fetch song safely
        try:
            song = Playlist.objects.get(id=song_id)
        except Playlist.DoesNotExist:
            return Response({"error": "Song not found"}, status=404)

        # Save rating — update if exists
        rating_obj, created = SongRating.objects.update_or_create(
            playlist=song,
            user_id=user_id,
            defaults={"rating": rating}
        )

        serializer = SongsRatingSerializer(rating_obj)
        return Response({"data" :serializer.data,
                         "message" : "Rated song successfully!!"}, status=200)
