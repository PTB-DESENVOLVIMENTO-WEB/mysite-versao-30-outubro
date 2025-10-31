from flask import current_app
from sendgrid import SendGridAPIClient
import json

def send_email_sendgrid(to_list, subject, html_content_body):
    """
    Envia e-mail com SendGrid usando um payload JSON manual
    para evitar bugs da classe helper 'Mail'.
    """
    
    config = current_app.config
    full_subject = f"{config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}"

    personalizations = [
        {
            "to": [{"email": email} for email in to_list]
        }
    ]

    data = {
        "personalizations": personalizations,
        "from": {
            "email": config['API_FROM']
        },
        "subject": full_subject,
        "content": [
            {
                "type": "text/html",
                "value": html_content_body
            }
        ]
    }


    try:
        sg = SendGridAPIClient(config['SENDGRID_API_KEY'])
        
        response = sg.client.mail.send.post(request_body=data)
        
        print(f"E-mail enviado para {to_list}, status: {response.status_code}")
        
    except Exception as e:
 
        print(f"Erro ao enviar e-mail: {e}")
        if hasattr(e, 'body'):
            print(f"Corpo da resposta do SendGrid: {e.body}")
