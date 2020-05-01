import stripe
from backend import config
from backend.db.models.purchase import Purchase
from backend.db import session
from backend.common.errors import Http400Error

stripe.api_key = config.STRIPE_API_KEY


def create_payment_intent(user, document_id, amount, currency, payment_method):
    purchase = Purchase()
    purchase.document_id = document_id
    purchase.user_id = user.id

    session.add(purchase)
    session.commit()

    intent = stripe.PaymentIntent.create(
        amount=100 * amount,
        currency=currency,
        payment_method_types=payment_method,
        receipt_email=user.email,
        metadata={
            'purchase_id': purchase.id
        }
    )

    purchase.payment_status = intent.status
    session.commit()

    return (intent.client_secret, purchase)

    # intent = {
    # "amount": 1035,
    # "amount_capturable": 0,
    # "amount_received": 0,
    # "application": null,
    # "application_fee_amount": null,
    # "canceled_at": null,
    # "cancellation_reason": null,
    # "capture_method": "automatic",
    # "charges": {
    #     "data": [],
    #     "has_more": false,
    #     "object": "list",
    #     "total_count": 0,
    #     "url": "/v1/charges?payment_intent=pi_1Gdv9MJtdDvmMFZWngADnQHW"
    # },
    # "client_secret": "pi_1Gdv9MJtdDvmMFZWngADnQHW_secret_OabcqyaN31BrlHZMWPYBmEgeW",
    # "confirmation_method": "automatic",
    # "created": 1588325236,
    # "currency": "usd",
    # "customer": null,
    # "description": null,
    # "id": "pi_1Gdv9MJtdDvmMFZWngADnQHW",
    # "invoice": null,
    # "last_payment_error": null,
    # "livemode": false,
    # "metadata": {},
    # "next_action": null,
    # "object": "payment_intent",
    # "on_behalf_of": null,
    # "payment_method": null,
    # "payment_method_options": {
    #     "card": {
    #     "installments": null,
    #     "request_three_d_secure": "automatic"
    #     }
    # },
    # "payment_method_types": [
    #     "card"
    # ],
    # "receipt_email": "nosuchip@gmail.com",
    # "review": null,
    # "setup_future_usage": null,
    # "shipping": null,
    # "source": null,
    # "statement_descriptor": null,
    # "statement_descriptor_suffix": null,
    # "status": "requires_payment_method",
    # "transfer_data": null,
    # "transfer_group": null
    # }


def handle_stripe_webhook(payload, signature):
    # payment_intent.amount_capturable_updated
    # payment_intent.canceled
    # payment_intent.created
    # payment_intent.payment_failed
    # payment_intent.processing
    # payment_intent.succeeded

    try:
        event = stripe.Webhook.construct_event(payload, signature, config.STRIPE_WEBHOOK_SECRET)
    except ValueError as ex:
        print('handle_stripe_webhook value error:', ex)
        raise Http400Error()
    except stripe.error.SignatureVerificationError as ex:
        print('handle_stripe_webhook signature error:', ex)
        raise Http400Error()

    print('webhook constructed event:', event)

    # if event.status == 'payment_intent.succeeded':
    #     pass
