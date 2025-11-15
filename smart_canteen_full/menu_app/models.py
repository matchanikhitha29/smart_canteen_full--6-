from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# ---------------------------
# CATEGORY CHOICES (Fixed)
# ---------------------------
CATEGORY_CHOICES = [
    ("Breakfast", "Breakfast"),
    ("Beverage", "Beverage"),
    ("Meal", "Meal"),
    ("Non-Veg", "Non-Veg"),
    ("Snacks", "Snacks"),
]


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    # FIX: restrict categories to fixed choices
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True
    )

    available = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to='menu_images/',
        blank=True,
        null=True
    )

    # FIX: rating always 0–5
    rating = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return self.name

    # Auto-clean category (avoid lowercase, wrong names)
    def save(self, *args, **kwargs):
        if self.category:
            self.category = self.category.strip().title()
        super().save(*args, **kwargs)



# ---------------------------
# ORDER MODEL
# ---------------------------
class Order(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id}"


# ---------------------------
# ORDER ITEM MODEL
# ---------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.item.name}"
