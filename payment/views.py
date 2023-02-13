import stripe
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse

from basket.basket import Basket
from orders.views import payment_confirmation

# Create your views here.

@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    stripe.api_key = 'sk_test_51MYXIwF5n0J2vH3GHpBvtX4qSlZCl72HkKFveYSEpoutxto73ziWm67taNhrqbNfTGm3UOt7lG48yenPVTeDK0Kf00ox5VMHog'
    intent = stripe.PaymentIntent.create(         #To'lov maqsadi
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    # print(payload)
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Ishlamaydigan hodisa turi {}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')