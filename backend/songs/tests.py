from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Playlist, SongRating

class PlaylistRatingTests(APITestCase):

    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user2 = User.objects.create_user(username="seconduser", password="password123")

        # Create test songs
        self.song1 = Playlist.objects.create(title="Song One")
        self.song2 = Playlist.objects.create(title="Song Two")

        # Add existing ratings
        SongRating.objects.create(playlist=self.song1, user=self.user, rating=5)
        SongRating.objects.create(playlist=self.song1, user=self.user2, rating=3)

        # Authenticated client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # ------------------- Playlist Fetch -------------------
    def test_get_playlist_with_ratings(self):
        """Test fetching a song returns all ratings"""
        response = self.client.get(f"/api/songs/{self.song1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Song One")
        self.assertEqual(len(response.data["ratings"]), 2)

    # ------------------- Get by title -------------------
    def test_get_by_title_success(self):
        """Test fetching songs by title"""
        response = self.client.get(f"/api/songs/by-title/?title=Song One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Song One")

    def test_get_by_title_no_title_param(self):
        """Test missing title query param"""
        response = self.client.get("/api/songs/by-title/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "title query param is required")

    def test_get_by_title_partial_match(self):
        """Test partial title match"""
        response = self.client.get(f"/api/songs/by-title/?title=Song")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # matches Song One and Song Two

    def test_get_by_title_no_match(self):
        """Test title not found"""
        response = self.client.get(f"/api/songs/by-title/?title=Nonexistent Song")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ------------------- Rate Song -------------------
    def test_rate_song_success(self):
        """Test posting a rating for a song"""
        data = {
            "song_id": self.song2.id,
            "user_id": self.user.id,
            "rating": 4
        }
        response = self.client.post("/api/ratings/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["rating"], 4)
        self.assertEqual(response.data["data"]["user"]["id"], self.user.id)
        self.assertEqual(response.data["data"]["playlist"], self.song2.id)

    def test_rate_song_update_existing(self):
        """Test updating existing rating"""
        data = {
            "song_id": self.song1.id,
            "user_id": self.user.id,
            "rating": 2
        }
        response = self.client.post("/api/ratings/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating_obj = SongRating.objects.get(playlist=self.song1, user=self.user)
        self.assertEqual(rating_obj.rating, 2)

    def test_rate_song_missing_fields(self):
        """Test missing fields"""
        data = {
            "song_id": self.song2.id,
            "rating": 4
        }
        response = self.client.post("/api/ratings/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_song_invalid_rating(self):
        """Test invalid rating (>5)"""
        data = {
            "song_id": self.song2.id,
            "user_id": self.user.id,
            "rating": 10
        }
        response = self.client.post("/api/ratings/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_song_nonexistent_song(self):
        """Test song_id does not exist"""
        data = {
            "song_id": 9999,
            "user_id": self.user.id,
            "rating": 3
        }
        print(data)
        response = self.client.post("/api/ratings/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
