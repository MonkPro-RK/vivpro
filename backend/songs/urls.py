from rest_framework import routers
from .views import PlaylistViewSet,SongRatingViewSet
from django.urls import path

router = routers.DefaultRouter()

song_rating_create = SongRatingViewSet.as_view({
    "post": "rate_the_song"
})

router.register(r"songs", PlaylistViewSet, basename="songs")
# router.register(r"rating", SongRatingViewSet, basename="rating")


urlpatterns = [

    # ONLY POST API for rating
    path("ratings/", song_rating_create, name="song-rating"),
] + router.urls
