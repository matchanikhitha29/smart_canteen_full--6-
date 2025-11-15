# Smart Canteen Menu (Django)

Features:
- Django + REST API (DRF)
- Bootstrap responsive UI
- Login & Registration
- Admin dashboard for orders and items
- Dark / Light mode toggle
- Search & filter menu
- Cart with add / update quantity / remove
- Sample menu seeding command

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # create admin
python manage.py seed_menu       # load sample items
python manage.py runserver
```

Open:

- Menu: http://127.0.0.1:8000/menu/
- Cart: http://127.0.0.1:8000/cart/
- Dashboard (staff only): http://127.0.0.1:8000/dashboard/
- API items: http://127.0.0.1:8000/api/items/
```
