from django.db import models
from django.contrib.auth.models import User

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Screen(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cinema.name} - {self.name}"

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # 片長（分鐘）
    release_date = models.DateField()
    image_url = models.CharField(max_length=500, null=True, blank=True, default="")  # ✅ 已補 default

    def __str__(self):
        return self.title


    def __str__(self):
        return self.title

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    screening_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} @ {self.screen.name} - {self.screening_time}"

class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)  # ✅ 從 Screening 改為 Screen
    seat_number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.screen.name} - {self.seat_number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 預約 {self.screening}"
