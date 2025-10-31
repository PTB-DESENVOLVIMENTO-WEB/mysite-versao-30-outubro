import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- NOSSAS NOVAS CONFIGURAÇÕES ---
    # Chaves do SendGrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    API_FROM = os.environ.get('API_FROM') # E-mail verificado no SendGrid
    
    # E-mail institucional do Aluno
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') 
    
    # Prontuário e Nome do Aluno
    STUDENT_ID = os.environ.get('STUDENT_ID')
    STUDENT_NAME = os.environ.get('STUDENT_NAME')
    
    # Prefixo do assunto do e-mail
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # ------------------------------------

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
