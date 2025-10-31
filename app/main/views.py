from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Role
from ..email import send_email_sendgrid # <-- IMPORTAMOS NOSSA FUNÇÃO

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # Cria o usuário
            user_role = Role.query.filter_by(name='User').first()
            if User.query.count() == 0: # Bônus: primeiro usuário é admin
                 user_role = Role.query.filter_by(name='Administrator').first()
            
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            
            # --- LÓGICA DE E-MAIL ADICIONADA ---
            config = current_app.config # Pega as configs (API_FROM, STUDENT_ID, etc)
            
            # Lista de destinatários (incondicional)
            destinatarios = [
                config['FLASKY_ADMIN'], # Seu e-mail institucional
                'flaskaulasweb@zohomail.com' # E-mail do professor
            ]
            new_user_name = form.name.data
            
            # Corpo do e-mail com dados do aluno
            html_body = f"""
                <h3>Novo Usuário Cadastrado!</h3>
                <p><strong>Prontuário do Aluno:</strong> {config['STUDENT_ID']}</p>
                <p><strong>Nome do Aluno:</strong> {config['STUDENT_NAME']}</p>
                <hr>
                <p><strong>Nome do novo usuário:</strong> {new_user_name}</p>
            """
            
            # Chama a função de envio
            send_email_sendgrid(
                to_list=destinatarios,
                subject='Novo usuário',
                html_content_body=html_body
            )
            # --- FIM DA LÓGICA DE E-MAIL ---
            
            session['known'] = False
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        return redirect(url_for('.index'))
        
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
