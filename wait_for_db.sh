#!/bin/sh

echo "⏳ Waiting for database to start..."
while ! nc -z db 3306; do
  sleep 1
done

echo "✅ Database is ready!"

# echo "🚀 Running migrations..."
# python manage.py migrate

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# ---- START SERVER CONDITIONALLY ----
if [ "$ENVIRONMENT" = "production" ]; then
  echo "🔥 Starting Gunicorn (Production Mode)..."
  gunicorn fin-lost-backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
  echo "💻 Starting Django Development Server..."
  python manage.py runserver 0.0.0.0:8000
fi
