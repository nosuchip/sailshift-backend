import stripe
from backend import config
from backend.db.models.purchase import Purchase
from backend.db import session, enums
from backend.common.errors import Http400Error
from backend.api.documents import document_controller
from backend.api.payments import purchase_controller
from backend.common.logger import logger

stripe.api_key = config.STRIPE_API_KEY


def create_payment_intent(user, document_id, amount, currency, payment_method):
    document = document_controller.get_document(document_id)

    if document.price != amount or currency != enums.Currencies.USD.value:
        raise Http400Error('Amount or currency is incorrect')

    purchase = Purchase()
    purchase.document_id = document_id
    purchase.user_id = user.id

    session().add(purchase)
    session().commit()

    intent = stripe.PaymentIntent.create(
        amount=int(100 * amount),
        currency=currency,
        payment_method_types=[payment_method],
        receipt_email=user.email,
        metadata={
            'purchase_id': purchase.id
        }
    )

    purchase.payment_status = intent.status
    purchase.payment_id = intent.id,
    purchase.payment_data = intent

    session().commit()

    return (intent.client_secret, purchase)


def handle_stripe_webhook(payload_as_string, signature):
    # payment_intent.amount_capturable_updated
    # payment_intent.canceled
    # payment_intent.created
    # payment_intent.payment_failed
    # payment_intent.processing
    # payment_intent.succeeded

    logger.info(">> handle_stripe_webhook, signature:", signature)
    logger.info(">> signature:", signature)
    logger.info(">> wh secret:", config.STRIPE_WEBHOOK_SECRET)
    logger.info(">> payload:", payload_as_string)

    try:
        event = stripe.Webhook.construct_event(payload_as_string, signature, config.STRIPE_WEBHOOK_SECRET)
    except ValueError as ex:
        logger.exception('handle_stripe_webhook value error:')
        logger.exception(ex)
        raise Http400Error()
    except stripe.error.SignatureVerificationError as ex:
        logger.exception('handle_stripe_webhook signature error:')
        logger.exception(ex)
        raise Http400Error()

    if event.type == 'payment_intent.succeeded':
        payment = event.data.object

        if payment.object == 'payment_intent':
            return purchase_controller.activate_purchase(payment.metadata.purchase_id, payment_status='success')
    elif event.type == 'payment_intent.payment_failed':
        purchase_controller.fail_purchase(payment.metadata.purchase_id)
        logger.exception("Payment failed")
        logger.exception(payload_as_string)
        error = event.data.object.last_payment_error
        raise Http400Error(error.message)
