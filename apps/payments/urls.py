from django.urls import path
from .views import CreatePaymentIntentView, stripe_webhook

urlpatterns = [
    path("payments/create-intent/", CreatePaymentIntentView.as_view()),
    path("payments/webhook/", stripe_webhook),
]
