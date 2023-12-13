from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer(), default=0)
    active = db.Column(db.Boolean())
    admin = db.Column(db.Boolean(), default=False)
    mfa_enabled = db.Column(db.Boolean(), default = False)
    otp_secret = db.Column(db.String(16))
    last_used_code = db.Column(db.String(16))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # prevents password from being read
    @property 
    def password(self):
        raise AttributeError('Password is not readable.')
    
    # transforms password into hashed password
    @password.setter
    def password(self, password):
        self.hashed_password=generate_password_hash(password)

    # checks if a given plaintext password is equal to the hashed password
    def verify_password(self, password):
        return check_password_hash(self.hashed_password,password)    
    
    #checks if a given otp is valid for the selected user
    def verify_totp(self, otp):
        return pyotp.TOTP(self.otp_secret).verify(otp)



class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    company = db.Column(db.String(40), nullable=False)
    job_title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Work')


    def __repr__(self):
        return f"Work('{self.start_date}', '{self.company}', '{self.job_title}')"

class Qualifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qualification = db.Column(db.String(40), nullable=False)
    grade = db.Column(db.String(10))
    year_obtained = db.Column(db.Integer, nullable=False)
    institution = db.Column(db.String(40), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Qualifications')


    def __repr__(self):
        return f"Qualification('{self.year_obtained}', '{self.institution}', '{self.grade}')"
    

class Hobbies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hobby = db.Column(db.String(15), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(128))
    image_license = db.Column(db.String(128))
    image_attribution = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Hobbies')


    def __repr__(self):
        return f"Hobbies('{self.hobby}')"

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text, nullable=False)
    repo_link = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Projects')

    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.author_id}')"

class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(15), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Skills')



    def __repr__(self):
        return f"Skill('{self.id}', '{self.skill}', '{self.author_id}')"

# table to handle the many to many relationship between projects and skills
class SkillsToProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Projects', backref='SkillsToProjects')
    skill = db.relationship('Skills', backref='SkillsToProjects')

    def __repr__(self):
        return f"SkillsToProject('{self.id}', '{self.skill_id}', '{self.project_id}')"

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(15), nullable=False)
    # column page determines which page the comment is associated to
    page_id = db.Column(db.Integer)
    # column page_id determines which row entry on certain pages the comment is associated to
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Comments')
    comment = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Comment('{self.id}', '{self.page}', '{self.page_id}', '{self.author_id}', '{self.comment}')"

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(15), nullable=False)
    page_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='Ratings')
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rating('{self.id}', '{self.page}','{self.page_id}', '{self.author_id}', '{self.rating}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))