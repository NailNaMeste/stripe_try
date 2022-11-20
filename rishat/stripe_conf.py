import stripe
from django.conf import settings

stripe.api_key = settings.PRIVATE_API_KEY


def set_public_key(request):
    return {'PUBLIC_API_KEY': settings.PUBLIC_API_KEY}
