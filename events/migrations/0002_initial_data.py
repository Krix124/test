from django.db import migrations
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def create_initial_data(apps, schema_editor):
    # Get models
    Event = apps.get_model('events', 'Event')
    User = apps.get_model('auth', 'User')
    
    # Create a test admin user
    admin_user = User.objects.create(
        username='admin',
        email='admin@example.com',
        password=make_password('admin123'),
        is_staff=True,
        is_superuser=True
    )

    # Create sample events
    events_data = [
        {
            'title': 'Tech Conference 2024',
            'description': 'Annual technology conference featuring the latest innovations',
            'date': timezone.now() + timezone.timedelta(days=30),
            'location': 'Convention Center',
            'max_participants': 200,
            'current_participants': 0,
        },
        {
            'title': 'Music Festival',
            'description': 'A day of live music performances and entertainment',
            'date': timezone.now() + timezone.timedelta(days=45),
            'location': 'City Park',
            'max_participants': 500,
            'current_participants': 0,
        },
        {
            'title': 'Workshop: Web Development',
            'description': 'Learn the basics of web development in this hands-on workshop',
            'date': timezone.now() + timezone.timedelta(days=15),
            'location': 'Tech Hub',
            'max_participants': 50,
            'current_participants': 0,
        }
    ]

    for event_data in events_data:
        Event.objects.create(**event_data)

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ] 