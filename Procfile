release: python manage.py migrate && python manage.py collectstatic --noinput && python -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@qrtist.com', 'adminqrtist')
    print('✅ Admin user created')
"
web: gunicorn qrtist.wsgi --workers 2 --threads 4 --timeout 120