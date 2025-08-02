from django.shortcuts import render
from django import forms
from rest_framework import viewsets, mixins, permissions
from .models import Movie, Screening, Booking
from .serializers import (
    MovieSerializer,
    ScreeningSerializer,
    BookingCreateSerializer,
    BookingReadSerializer,
)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ScreeningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Screening.objects.select_related("movie", "screen__cinema")
    serializer_class = ScreeningSerializer

class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("screening__movie")

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingReadSerializer
    


from django.shortcuts import render, get_object_or_404
from .models import Movie, Screening, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def movie_list(request):
    movies = Movie.objects.all()
    print("✅ movies:", movies)  # ← 看終端機有沒有印出資料
    return render(request, "movie_list.html", {"movies": movies})

def screening_list(request, movie_id):
    screenings = Screening.objects.filter(movie_id=movie_id)
    return render(request, "screening_list.html", {"screenings": screenings, "movie_id": movie_id})

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Screening, Seat, Booking

@login_required


def seat_booking(request, screening_id):
    screening = get_object_or_404(Screening, pk=screening_id)
    screen = screening.screen  # ✅ 從場次取得影廳
    seats = Seat.objects.filter(screen=screen).order_by("seat_number")  # ✅ 正確欄位為 screen

    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")  # ['1', '2', '3']
        seat_objs = Seat.objects.filter(pk__in=selected_seats, screen=screen, is_reserved=False)

        if seat_objs.count() != len(selected_seats):
            return render(request, "seat_booking.html", {
                "screening": screening,
                "seats": seats,
                "error": "有座位已被預訂，請重新選擇。"
            })

        booking = Booking.objects.create(user=request.user, screening=screening)
        booking.seats.set(seat_objs)
        seat_objs.update(is_reserved=True)

        return HttpResponseRedirect(reverse("movie_list"))

    return render(request, "seat_booking.html", {
        "screening": screening,
        "seats": seats,
    })


from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 註冊完自動登入
            return redirect("movie_list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


