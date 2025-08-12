FROM python:3.11-slim                 
ENV PYTHONDONTWRITEBYTECODE=1         
ENV PYTHONUNBUFFERED=1                
WORKDIR /app                          

COPY requirements.txt .             
RUN pip install --upgrade pip \
 && pip install -r requirements.txt   

COPY . .                              
# 你有使用 Django staticfiles 才加（沒有就刪掉）
# RUN python manage.py collectstatic --noinput

# Cloud Run 會注入環境變數 PORT；gunicorn 綁定該埠
CMD gunicorn cinema_booking.wsgi:application --bind 0.0.0.0:${PORT:-8080}
