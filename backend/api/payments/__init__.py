from flask import Blueprint, request, g
from backend.common.decorators import validate_schema, login_required
from backend.api.payments.schema import CreatePaymentIntentSchema
from backend.api.payments import payment_controller
from backend.api.payments import purchase_controller
from backend.common.decorators import user_required
from backend.common.errors import Http404Error

blueprint = Blueprint('payments', __name__, url_prefix='/api/payments')


@blueprint.route('/prepay', methods=['POST'])
@login_required
@validate_schema(CreatePaymentIntentSchema)
def create_payment_intent(params):
    (intent_client_secret, purchase) = payment_controller.create_payment_intent(g.user, **params)

    return {'client_secret': intent_client_secret}


@blueprint.route('/stripe/webhook', methods=['POST'])
def handle_stripe_webhook():
    signature = request.headers.get('Stripe-Signature', None)
    payload_str = request.data.decode("utf-8")

    payment_controller.handle_stripe_webhook(payload_str, signature)

    return {'success': True}


@blueprint.route('/check/<payment_id>', methods=['GET'])
@user_required
def check_user_document_payment(payment_id):
    purchase = purchase_controller.get_purchase(payment_id=payment_id)

    if not purchase or purchase.user_id != g.user.id:
        raise Http404Error('Purchase not found')

    return {'purchase': purchase.to_json()}
