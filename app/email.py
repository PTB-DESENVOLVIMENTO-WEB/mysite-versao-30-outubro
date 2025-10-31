from flask import current_app
from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail, Email

def send_email_sendgrid(to_list, subject, html_content_body):
    """Envia e-mail com SendGrid de forma robusta."""
    
    config = current_app.config
    full_subject = f"{config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}"

    from_email = Email(config['API_FROM'])

    to_emails = [Email(email) for email in to_list]

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=full_subject,
        html_content=html_content_body
    )

    try:
        sg = SendGridAPIClient(config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(f"E-mail enviado para {to_list}, status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
