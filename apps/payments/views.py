import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Payment
from apps.orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.payment_status == "paid":
            return Response({"error": "Order already paid"}, status=400)

        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            metadata={"order_id": order.id},
        )

        Payment.objects.create(
            order=order,
            stripe_payment_intent_id=intent.id,
            amount=order.total_amount,
            currency="usd",
            status="pending",
        )

        return Response(
            {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
            },
            status=status.HTTP_201_CREATED,
        )

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return JsonResponse({"error": "Invalid webhook"}, status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]

        payment = Payment.objects.get(stripe_payment_intent_id=intent.id)
        order = payment.order

        payment.status = "succeeded"
        payment.save()

        order.payment_status = "paid"
        order.order_status = "paid"
        order.save()

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]

        payment = Payment.objects.get(stripe_payment_intent_id=intent.id)
        payment.status = "failed"
        payment.save()

    return JsonResponse({"status": "success"})