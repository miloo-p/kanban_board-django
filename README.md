# Kanban Board API

REST-API für ein Kanban-Board mit Django und Django REST Framework.

## Setup

Voraussetzung: Python 3.12 oder neuer.

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

Der vorletzte Befehl erzeugt die Datei `.env` mit einem neuen `SECRET_KEY`.

Die API läuft unter `http://127.0.0.1:8000/api/`.
