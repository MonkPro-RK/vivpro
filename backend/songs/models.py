from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Playlist(models.Model):
    song_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    mode = models.IntegerField(null=True)
    acousticness = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    duration_ms = models.IntegerField(null=True)
    num_sections = models.IntegerField(null=True)
    num_segments = models.IntegerField(null=True)
                                   

    def __str__(self):
        return self.title


class SongRating(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        unique_together = ('playlist', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.playlist.title}: {self.rating}"
