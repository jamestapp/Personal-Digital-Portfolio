from flask import Flask, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
#import os
from flask_mail import Mail
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['SECRET_KEY'] = '2701d8a6faa11ce6955d9b0430bc3ff08982b25edb01bc1d'
app.config['SECURITY_PASSWORD_SALT'] = 'sw6YcWv6Ej5t0hfQTa3ed9SK6rKGxX7bz6PigTtXtaYyHTVnh96wMsV0OWUCaNZ'

#basedir = os.path.abspath(os.path.dirname(__file__))

# old db connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')

# mysql db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22076087:mi~*4Devi|:Khxgo@csmysql.cs.cf.ac.uk:3306/c22076087_flask_project_db'

db = SQLAlchemy(app)
#set up flask admin
class MyHomeView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You need admin permissions to access this page')
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name='DigitalPortfolio', index_view=MyHomeView())

#set up mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'FlaskCMT120@gmail.com'
app.config['MAIL_PASSWORD'] = 'utcyvzxbpgmexqkd'
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

#set up qr codes
QRcode(app)

#set up flask login
login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes, models