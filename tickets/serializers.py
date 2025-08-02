from rest_framework import serializers
from .models import Movie, Screening, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class ScreeningSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    screen = serializers.StringRelatedField()

    class Meta:
        model = Screening
        fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_reserved"]

class BookingCreateSerializer(serializers.Serializer):
    screening_id = serializers.IntegerField()
    seat_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate(self, attrs):
        from django.db import transaction
        from .models import Screening, Seat

        screening_id = attrs["screening_id"]
        seat_ids = attrs["seat_ids"]

        try:
            screening = Screening.objects.get(pk=screening_id)
        except Screening.DoesNotExist:
            raise serializers.ValidationError("找不到此場次")

        with transaction.atomic():
            seats = Seat.objects.select_for_update().filter(pk__in=seat_ids, screening=screening)
            if seats.count() != len(seat_ids):
                raise serializers.ValidationError("座位資訊有誤")
            if any(s.is_reserved for s in seats):
                raise serializers.ValidationError("有座位已被預訂")

            attrs["screening"] = screening
            attrs["seats"] = seats
        return attrs

    def create(self, validated_data):
        from django.db import transaction
        from .models import Booking

        user = self.context["request"].user
        screening = validated_data["screening"]
        seats = validated_data["seats"]

        with transaction.atomic():
            booking = Booking.objects.create(user=user, screening=screening)
            booking.seats.set(seats)
            Seat.objects.filter(pk__in=[s.id for s in seats]).update(is_reserved=True)

        return booking

class BookingReadSerializer(serializers.ModelSerializer):
    screening = ScreeningSerializer()
    seats = SeatSerializer(many=True)

    class Meta:
        model = Booking
        fields = ["id", "screening", "seats", "booked_at"]
