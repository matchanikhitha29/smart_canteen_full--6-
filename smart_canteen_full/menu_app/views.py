from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Sum
from django.contrib import messages

from .models import Item, Order, OrderItem
from .forms import RegisterForm, SearchForm, ItemForm   # ← includes new form


# ---------------------------
# General Helpers
# ---------------------------
def home(request):
    return render(request, 'home.html')


def menu_redirect(request):
    return redirect('home')



def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ---------------------------
# Menu Page (User)
# ---------------------------
@login_required(login_url='login')
def menu_list(request):

    items = Item.objects.all()

    # --- Search ---
    q = request.GET.get("q")
    if q:
        items = items.filter(name__icontains=q)

    # --- Category filter ---
    selected_category = request.GET.get("category")
    if selected_category and selected_category != "":
        items = items.filter(category=selected_category)

    # --- Available only ---
    available_only = request.GET.get("available_only")
    if available_only == "on":
        items = items.filter(available=True)

    # --- Categories List ---
    categories = Item.objects.values_list("category", flat=True).distinct()

    # --- Cart Total ---
    cart = _get_cart(request)
    total = Decimal("0.00")

    for item_id, qty in cart.items():
        try:
            item = Item.objects.get(id=item_id)
            total += item.price * qty
        except Item.DoesNotExist:
            pass

    return render(request, "menu.html", {
        "items": items,
        "categories": categories,
        "selected_category": selected_category,
        "cart_total": total,
        "cart_count": sum(cart.values()),

        # send GET values back to template
        "form": request.GET,  
    })



# ---------------------------
# Cart Logic
# ---------------------------
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id, available=True)
    cart = _get_cart(request)
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    _save_cart(request, cart)
    return redirect('menu_list')


def update_cart(request, item_id, action):
    cart = _get_cart(request)
    key = str(item_id)

    if key in cart:
        if action == 'inc':
            cart[key] += 1
        elif action == 'dec':
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]

    _save_cart(request, cart)
    return redirect('cart_view')


def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    cart.pop(str(item_id), None)
    _save_cart(request, cart)
    return redirect('cart_view')


def cart_view(request):
    cart = _get_cart(request)
    cart_items = []
    total = Decimal('0.00')

    for item_id, qty in cart.items():
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            continue

        line_total = item.price * qty
        total += line_total

        cart_items.append({
            'item': item,
            'quantity': qty,
            'line_total': line_total,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)


# ---------------------------
# Order Placement
# ---------------------------
@login_required
def place_order(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('menu_list')

    order = Order.objects.create(user=request.user, total_price=0)
    total = Decimal('0.00')

    for item_id, qty in cart.items():
        item = get_object_or_404(Item, id=item_id)
        OrderItem.objects.create(order=order, item=item, quantity=qty)
        total += item.price * qty

    order.total_price = total
    order.save()

    _save_cart(request, {})
    return render(request, 'order_success.html', {'order': order})


# ---------------------------
# Admin Toggle Item Availability
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def toggle_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.available = not item.available
    item.save()
    return redirect('menu_list')


# ---------------------------
# Dashboard (Admin)
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:10]

    top_items = (
        OrderItem.objects
        .values('item__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'top_items': top_items,
    }
    return render(request, 'dashboard.html', context)


# ---------------------------
# Register User
# ---------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')   # redirect to login page
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})



# ---------------------------
# Manage Items (Admin)
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def manage_items(request):
    items = Item.objects.all().order_by('name')
    return render(request, 'items/manage_list.html', {'items': items})


@user_passes_test(lambda u: u.is_staff)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_items')
    else:
        form = ItemForm()

    return render(request, 'items/item_form.html', {
        'form': form,
        'is_edit': False
    })


@user_passes_test(lambda u: u.is_staff)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/item_form.html', {
        'form': form,
        'is_edit': True,
        'item': item
    })

def login_required_popup(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login first to continue")
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap