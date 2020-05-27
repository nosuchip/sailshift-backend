from os import path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sendgrid
from sendgrid.helpers.mail import Email, To, Mail
from backend import config

jinja_loader = FileSystemLoader([
    path.join(path.dirname(__file__), '..', 'templates')
])
env = Environment(
    loader=jinja_loader,
    autoescape=select_autoescape(['html', 'xml', 'jinja2'])
)

sendgridClient = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)


def render_template(template_name, context=None):
    if not template_name.endswith('.jinja2'):
        template_name += '.jinja2'

    template = env.get_template(template_name)
    return template.render(**(context or {}))


def send(to, template, context=None, subject=None):
    mail = Mail(
        from_email=Email(config.EMAIL_FROM_ADDRESS),
        to_emails=To(to),
        html_content=render_template(template, context or {}),
        subject=subject
    )

    response = sendgridClient.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)
