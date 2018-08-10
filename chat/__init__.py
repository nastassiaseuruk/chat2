from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)


# TODO: create logs
# from logging.handlers import SMTPHandler
# from logging.handlers import RotatingFileHandler
# import os
# if not chat.debug:
#     if chat.config['MAIL_SERVER']:
#         auth = None
#         if chat.config['MAIL_USERNAME'] or chat.config['MAIL_PASSWORD']:
#             auth = (chat.config['MAIL_USERNAME'], chat.config['MAIL_PASSWORD'])
#         secure = None
#         if chat.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(chat.config['MAIL_SERVER'], chat.config['MAIL_PORT']),
#             fromaddr='no-reply@' + chat.config['MAIL_SERVER'],
#             toaddrs=chat.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         chat.logger.addHandler(mail_handler)
#
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/chat.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     chat.logger.addHandler(file_handler)
#
#     chat.logger.setLevel(logging.INFO)
#     chat.logger.info('Microblog startup')
from chat import routes, models, errors
