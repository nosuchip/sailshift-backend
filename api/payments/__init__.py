from flask import Blueprint, request, g
from backend.common.decorators import validate_schema, login_required
from backend.api.payments.schema import CreatePaymentIntentSchema
from backend.api.payments import payment_controller

blueprint = Blueprint('payments', __name__, url_prefix='/api/payments')


@blueprint.route('/prepay', methods=['POST'])
@login_required
@validate_schema(CreatePaymentIntentSchema)
def create_payment_intent(params):
    (intent_client_secret, purchase) = payment_controller.create_payment_intent(g.user, **params)

    return {'client_secret': intent_client_secret}


@blueprint.route('/stripe/webhook', methods=['POST'])
def handle_stripe_webhook():
    signature = request.headers['HTTP_STRIPE_SIGNATURE']
    payment_controller.handle_stripe_webhook(request.json, signature)
