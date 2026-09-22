#views.py
#Name: Sion Zhan (sszhan24@bu.edu), 9/17/2026
#Description: Views for the restaurant app.

from django.shortcuts import render
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

def main(request):
    """Display the restaurant's main page. request: the HTTP request
    object sent by the browser."""

    template_name = "restaurant/main.html"

    return render(request, template_name)

def order(request):
    """display the online order form with a randomly chosen daily special. request: the HTTP request object
    sent by the browser."""

    template_name = "restaurant/order.html"
    specials = [
        {"name": "Truffle Mushroom Pizza", "description": "Natural mushrooms, truffle "
        "oil, mozzarella", "price": 15.99},
        {"name": "Spicy Miso Ramen", "description": "Rich miso broth, chili "
        "oil, delicate egg", "price": 12.99},
        {"name": "Lobsta Rolla", "description": "Fresh Maine Lobster, butter, "
        "toasted bun", "price": 18.99},
        {"name": "Burrito Bowl", "description": "Grilled chicken or beef, rice, beans, "
        "guacamole, salsa verde", "price": 11.25},
    ]

    daily_special = random.choice(specials)

    context = {
        'daily_special': daily_special,
    }

    return render(request, template_name, context)

def confirmation(request):
    """Process submitted order and display confirmation page.
    request: the HTTP request object, expected to contain POST data for
    the customer's name and chosen menu items."""

    template_name = "restaurant/confirmation.html"

    #prices for regular menu items. Keys match values used on checkboxes in
    #order.html
    item_prices = {
        "Margherita Pizza": 15.00,
        "House Burger": 12.50,
        "Caesar Salad": 9.00,
    }

    #toppings prices, keyed by topping name from order.html
    topping_prices = {
        "Extra Cheese": 1.50,
        "Pepperoni": 2.00,
        "Mushrooms": 1.00,
    }

    #collect items that wer checked
    ordered_items = []
    total = 0.0

    #regular items
    checked_items = request.POST.getlist('items')

    #pizza toppings, only relevant if pizza was actually ordered
    topping = []
    if "Margherita Pizza" in checked_items:
        toppings = request.POST.getlist('pizza_toppings')

    for name in checked_items:
        #check if a hard-coded menu item
        if name in item_prices:
            price = item_prices[name]
            item_toppings = toppings if name == "Margherita Pizza" else[]

            #add topping prices to pizza total
            topping_cost = sum(topping_prices[t] for t in item_toppings)
            price += topping_cost

            ordered_items.append({
                "name": name,
                "price": price,
                "options": item_toppings
            })
            total += price
        else:
            #otherwise has to be daily special
            price = float(request.POST.get("daily_special_price", 0))
            ordered_items.append({
                "name": name,
                "price": price,
                "options": [],
            })
            total += price
    
    #customer info
    customer = {
        "name": request.POST.get("name", ""),
        "phone": request.POST.get("phone", ""),
        "email": request.POST.get("email", ""),
    }

    instructions = request.POST.get("instructions", "")

    #ready time, ranges from 30 to 60 minutes
    minutes = random.randint(30, 60)
    ready_time = timezone.localtime() + timedelta(minutes=minutes)

    context = {
        "ordered_items": ordered_items,
        "total": total,
        "customer": customer,
        "instructions": instructions,
        "ready_time": ready_time,
    }


    return render(request, template_name, context)