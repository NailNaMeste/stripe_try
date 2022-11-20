from django.urls import path

from .views import BuyView, ItemView, IndexPage

urlpatterns = [
    path('buy/<int:pk>/', BuyView.as_view(), name='buy'),
    path('items/<int:pk>/', ItemView.as_view(), name='items'),
    path('', IndexPage.as_view(), name='index'),
    # path('/create-payment-intent/', PaymentIntentApiView.as_view(), name='payment'),
    # path('checkout/', Checkout.as_view(), name='checkout')
]