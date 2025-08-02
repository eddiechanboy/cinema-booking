from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ScreeningViewSet, BookingViewSet
from . import views
from django.contrib.auth import views as auth_views

# ✅ 設定 API 路由器
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"screenings", ScreeningViewSet)
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    # ✅ 首頁：導向電影清單（HTML）
    path("", views.movie_list, name="home"),

    # ✅ API 路徑
    path("api/", include(router.urls)),

    # ✅ 使用者系統
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="movie_list"), name="logout"),

    # ✅ HTML 頁面路由
    path("movies/html/", views.movie_list, name="movie_list"),
    path("screenings/html/<int:movie_id>/", views.screening_list, name="screening_list"),
    path("book/html/<int:screening_id>/", views.seat_booking, name="seat_booking"),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
