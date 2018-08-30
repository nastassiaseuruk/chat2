from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from chat import app, db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='user', lazy=True)

    def __str__(self):
        return self.username or ""

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class FilteredWords(db.Model):
    __tablename__ = 'filteredwords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    deleted = db.Column(db.Boolean, default=False)

    def validate(self):
        import pudb;pu.db
        splited_words = self.text.split()
        filtered_words = FilteredWords.query.all()
        for sw in splited_words:
            for fw in filtered_words:
                if fw == sw:
                    sw = "***"
                else:
                    continue
        self.text = splited_words.join('')
        self.save()

    def delete(self):
        self.deleted = True

    def __str__(self):
        return self.text or ""

        
class FilteredWords(db.Model):
    __tablename__ = 'filteredwords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String)
