# Kanban Board API

REST API for a Kanban board built with Django and Django REST Framework.

## Setup

Requirement: Python 3.12 or newer.

```bash
git clone https://github.com/miloo-p/kanban_board-django.git
cd kanban_board-django

python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate

python -m pip install -r requirements.txt

python -c "from django.core.management.utils import get_random_secret_key as k; open('.env', 'w').write('SECRET_KEY=' + chr(39) + k() + chr(39) + chr(10))"

python manage.py migrate
python manage.py runserver
```

The third-to-last command creates the `.env` file with a new `SECRET_KEY`.

The API runs at `http://127.0.0.1:8000/api/`.
