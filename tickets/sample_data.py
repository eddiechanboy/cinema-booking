from tickets.models import Movie, Cinema, Screen, Screening, Seat
from django.utils import timezone
from datetime import timedelta
from django.db import transaction, connection

def load_sample_data_v2():
    print("🔍 當前資料庫連線資訊：")
    for k, v in connection.settings_dict.items():
        print(f"{k}: {v}")

    try:
        with transaction.atomic():
            # 建立電影院與放映廳
            cinema = Cinema.objects.create(name="信義威秀", location="台北市信義區")
            screen1 = Screen.objects.create(cinema=cinema, name="1廳", capacity=20)
            screen2 = Screen.objects.create(cinema=cinema, name="2廳", capacity=20)
            screen3 = Screen.objects.create(cinema=cinema, name="3廳", capacity=20)

            # 建立電影與場次（含圖片）
            movies_data = [
                {
                    "title": "星際效應",
                    "desc": "穿越蟲洞拯救地球",
                    "duration": 169,
                    "img": "https://leftymovie.com/wp-content/uploads/2014/11/1415509592-165493312_n.jpg"
                },
                {
                    "title": "奧本海默",
                    "desc": "原子彈之父的傳記",
                    "duration": 180,
                    "img": "https://upload.wikimedia.org/wikipedia/en/8/88/Oppenheimer_%28film%29.jpg"
                },
                {
                    "title": "芭比",
                    "desc": "粉紅世界的奇幻之旅",
                    "duration": 120,
                    "img": "https://upload.wikimedia.org/wikipedia/en/0/0b/Barbie_2023_poster.jpg"
                }
            ]
            screens = [screen1, screen2, screen3]

            for i, movie_data in enumerate(movies_data):
                movie = Movie.objects.create(
                    title=movie_data["title"],
                    description=movie_data["desc"],
                    duration=movie_data["duration"],
                    release_date="2024-01-01",
                    image_url=movie_data["img"]
                )

                screening = Screening.objects.create(
                    movie=movie,
                    screen=screens[i],
                    screening_time=timezone.now() + timedelta(days=i)
                )

                for j in range(1, 21):
                    Seat.objects.create(screening=screening, seat_number=f"A{j}")

            print("✅ 成功建立 3 部電影、3 個場次與各 20 個座位")

            print("📦 目前資料庫內容：")
            print("Movies:", Movie.objects.count())
            print("Cinemas:", Cinema.objects.count())
            print("Screens:", Screen.objects.count())
            print("Screenings:", Screening.objects.count())
            print("Seats:", Seat.objects.count())

    except Exception as e:
        print("❌ 發生錯誤：", e)
