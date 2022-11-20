from django.http import Http404
from django.views.generic import TemplateView
from rest_framework.response import Response

from rest_framework.views import APIView

from rishat.stripe_conf import stripe
from .models import Item


class BuyView(APIView):
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        return Response(data=session)


class ItemView(TemplateView):
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            item = Item.objects.get(pk=pk)
            return {"item": item}
        raise Http404


class IndexPage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        items = Item.objects.all()
        return {"items": items}
