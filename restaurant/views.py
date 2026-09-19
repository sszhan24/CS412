#views.py
#Name: Sion Zhan (sszhan24@bu.edu), 9/17/2026
#Description: Views for the restaurant app.

from django.shortcuts import render
import random

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

    return render(request, template_name)