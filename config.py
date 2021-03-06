import os


class Config(object):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@127.0.0.1:5432/chat2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['s-nastya23@mail.ru']
