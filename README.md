# Event Registration System

A Django-based event registration system that allows users to register for events and administrators to manage registrations.

## Features

- User Authentication (Register/Login)
- Event Creation and Management
- Event Registration with Payment Proof Upload
- Admin Dashboard with Statistics
- Registration Approval System
- Responsive Design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/event-registration.git
cd event-registration
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

### For Users
- Register an account at `/register/`
- Browse events at the homepage
- Register for events by uploading payment proof
- View registration status in event details

### For Administrators
- Access admin dashboard at `/dashboard/`
- Create new events at `/event/new/`
- Manage registrations at `/manage-registrations/`
- Access Django admin at `/admin/`

## Security Notes

- Replace the `SECRET_KEY` in settings.py with a secure key in production
- Set `DEBUG = False` in production
- Configure proper database settings for production
- Set up proper static and media file serving in production

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details 