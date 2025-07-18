#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@slidecraft.ai').exists():
    User.objects.create_superuser('admin@slidecraft.ai', 'admin@slidecraft.ai', 'admin123')
"

echo "✅ SlideCraft AI Backend deployed successfully with Google Gemini (FREE)!"
