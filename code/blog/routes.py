from flask import render_template, url_for, request, redirect, flash
from blog import app, db, admin, mail
from blog.models import User, Work, Qualifications, Hobbies, Projects, Skills, SkillsToProjects, Comments, Ratings
from blog.forms import RegistrationForm, LoginForm, CommentForm, RatingForm, ForgotForm, PasswordRecoveryForm, MFAForm, VerifyPasswordForm, ImageUploadForm, ImageDeleteForm, ChangePasswordForm, UpdateDetailsForm
from flask_login import login_user, logout_user, login_required, login_manager, current_user
import uuid as uuid
import os
from flask_admin.contrib.sqla import ModelView
from flask_admin import form, BaseView, expose
from flask_admin.menu import MenuLink
from flask_mail import Message
from blog.token import generate_email_confirmation_token, generate_password_confirmation_token, confirm_email_token, confirm_password_token
from datetime import datetime
import base64
import pyotp
from wtforms.validators import NumberRange
from blog.customValidators import minDateCheck, maxDateCheck, startBeforeEnd, skillProjectComboValid, imageFileValid

current_dir = os.path.abspath(os.path.dirname(__file__))
image_file_path = os.path.join(current_dir, 'static', 'img')

class PortfolioModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.admin
	
	def inaccessible_callback(self, name, **kwargs):
		flash('You need admin permissions to access this page', 'alert-info')
		return redirect(url_for('login'))
		
class UserModelView(PortfolioModelView):
	can_create=False
	column_exclude_list = ['hashed_password', 'otp_secret', 'last_used_code']

class WorkModelView(PortfolioModelView):
	form_args = {
		'start_date': {
			'validators': [minDateCheck, maxDateCheck, startBeforeEnd]
		},
		'end_date':{
			'validators': [minDateCheck, maxDateCheck]
		}
	}
	
class QualificationModelView(PortfolioModelView):
	form_args = {
		'year_obtained': {
			'validators': [NumberRange(min=1995, max=2075, message='Please enter a valid year')]
		}
	}

class HobbiesModelView(PortfolioModelView):
	form_extra_fields = {
		'path': form.ImageUploadField('img', base_path=image_file_path)
    }
	form_args = {
		'image_file': {
			'validators': [imageFileValid]
		}
	}

class ProjectModelView(PortfolioModelView):
	form_columns = ['title', 'content', 'repo_link', 'author']

class SkillsModelView(PortfolioModelView):
	form_columns = ['skill', 'author']

class SkillsToProjectsView(PortfolioModelView):
	form_args = {
		'project': {
			'validators': [skillProjectComboValid]
		}
	}

class ImagesView(BaseView):
	@expose('/', methods=['GET', 'POST'])
	def images(self):
		upload_form = ImageUploadForm()
		delete_form = ImageDeleteForm()
		delete_form.delete_file.choices = [(file, file) for file in os.listdir(os.path.join('blog', 'static', 'img'))]
		if upload_form.validate_on_submit():
			try:
				request.files['pic'].save(image_file_path)
				flash("Upload successful!", "alert-success")
			except:
				flash('There was a problem uploading this file, please try again', 'alert-warning')
			return redirect(url_for('images.images'))
		if delete_form.validate_on_submit():
			os.remove(os.path.join(image_file_path, delete_form.delete_file.data))
			flash("Delete successful!", "alert-success")
			return redirect(url_for('images.images'))
		return self.render('admin/images.html', upload_form=upload_form, delete_form=delete_form)

admin.add_view(UserModelView(User, db.session))
admin.add_view(QualificationModelView(Qualifications, db.session))
admin.add_view(WorkModelView(Work, db.session))
admin.add_view(HobbiesModelView(Hobbies, db.session))
admin.add_view(ProjectModelView(Projects, db.session))
admin.add_view(SkillsModelView(Skills, db.session))
admin.add_view(SkillsToProjectsView(SkillsToProjects, db.session))
admin.add_view(PortfolioModelView(Comments, db.session))
admin.add_view(PortfolioModelView(Ratings, db.session))
admin.add_view(ImagesView(name='Images', endpoint='images'))
admin.add_link(MenuLink(name='Homepage', url='/', category='Main Site'))
admin.add_link(MenuLink(name='Qualifications', url='/qualifications', category='Main Site'))
admin.add_link(MenuLink(name='Work', url='/work-list', category='Main Site'))
admin.add_link(MenuLink(name='Projects', url='/project-list', category='Main Site'))
admin.add_link(MenuLink(name='Skills', url='/skill-list', category='Main Site'))
admin.add_link(MenuLink(name='Hobbies', url='/hobbies', category='Main Site'))

login_manager.login_view = 'login'

# flask security views

def addComment(commentForm, pageType, object_id=None):
	comment = Comments(page=pageType, author_id=current_user.id, comment=commentForm.comment.data, page_id=object_id)
	db.session.add(comment)
	db.session.commit()
	flash('Comment added', 'alert-success')

def addRating(ratingForm, pageType, object_id=None):
	# pageType dertermines which area of the site the comments are associated with
	# currentPage determines where the user is sent next after submitting a comment
	userRating = Ratings.query.filter(Ratings.author_id == current_user.id, Ratings.page == pageType, Ratings.page_id == object_id).first()
	if userRating:
		userRating.rating = ratingForm.rating.data
		db.session.commit()
		flash('Rating changed', 'alert-success')
	else:
		# search the db to see if the user has already rated the page
		userRating = Ratings(page=pageType, page_id=object_id, author_id=current_user.id, rating=ratingForm.rating.data)
		flash('Rating updated', 'alert-success')
		db.session.add(userRating)
		db.session.commit()


# Navbar page routes
@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/qualifications", methods=['GET', 'POST'])
def qualifications():
	qualifications = Qualifications.query.order_by(Qualifications.year_obtained.desc()).all()
	commentForm = CommentForm()
	ratingForm = RatingForm()
	comments = Comments.query.filter(Comments.page == 'qualifications').order_by(Comments.comment_time.asc()).all()
	ratingsList = Ratings.query.filter(Ratings.page == 'qualifications').all()
	if ratingsList:
		overallRating = round(sum(rating.rating for rating in ratingsList) / len(ratingsList), 2)
	else:
		overallRating = 0
	# if else to prevent division by 0
	if commentForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to add a comment', 'alert-info')
			return redirect(url_for('login')) 
		addComment(commentForm, 'qualifications')
		return redirect(url_for('qualifications'))
	if ratingForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to submit a rating', 'alert-info')
			return redirect(url_for('login')) 
		addRating(ratingForm, 'qualifications')
		return redirect(url_for('qualifications'))
	return render_template('qualifications.html', title='qualifications', qualifications=qualifications, commentForm=commentForm, ratingForm=ratingForm, comments=comments, rating=overallRating)

@app.route("/project-list", methods=['GET', 'POST'])
def project_list():
	projects = Projects.query.all()
	return render_template('project-list.html', title='project', projects=projects)

@app.route("/work-list", methods=['GET', 'POST'])
def work_list():
	works = Work.query.all()
	return render_template('work-list.html', title='work', works=works)

@app.route("/skill-list", methods=['GET', 'POST'])
def skill_list():
	skills = Skills.query.all()
	commentForm = CommentForm()
	ratingForm = RatingForm()
	comments = Comments.query.filter(Comments.page == 'skill_list').order_by(Comments.comment_time.asc()).all()
	ratingsList = Ratings.query.filter(Ratings.page == 'skill_list').all()
	if ratingsList:
		overallRating = round(sum(rating.rating for rating in ratingsList) / len(ratingsList), 2)
	else:
		overallRating = 0
	# if else to prevent division by 0
	if commentForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to add a comment', 'alert-info')
			return redirect(url_for('login')) 
		addComment(commentForm, 'skill_list')
		return redirect(url_for('skill_list'))
	if ratingForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to submit a rating', 'alert-info')
			return redirect(url_for('login')) 
		addRating(ratingForm, 'skill_list')
		return redirect(url_for('skill_list'))
	return render_template('skill.html', title='skill', skills=skills, commentForm=commentForm, ratingForm=ratingForm, comments=comments, rating=overallRating)

@app.route("/hobbies", methods=['GET', 'POST'])
def hobbies():
	hobby_list = Hobbies.query.all() 
	commentForm = CommentForm()
	ratingForm = RatingForm()
	comments = Comments.query.filter(Comments.page == 'hobbies').order_by(Comments.comment_time.asc()).all()
	ratingsList = Ratings.query.filter(Ratings.page == 'hobbies').all()
	if ratingsList:
		overallRating = round(sum(rating.rating for rating in ratingsList) / len(ratingsList), 2)
	else:
		overallRating = 0
	# if else to prevent division by 0
	if commentForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to add a comment', 'alert-info')
			return redirect(url_for('login')) 
		addComment(commentForm, 'hobbies')
		return redirect(url_for('hobbies'))
	if ratingForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to submit a rating', 'alert-info')
			return redirect(url_for('login')) 
		addRating(ratingForm, 'hobbies')
		return redirect(url_for('hobbies'))
	return render_template('hobbies.html', hobby_list=hobby_list, form=form, commentForm=commentForm, ratingForm=ratingForm, comments=comments, rating=overallRating)	
	
@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		emailUser = User.query.filter_by(email=form.email.data).first()
		usernameUser = User.query.filter_by(username=form.username.data).first()
		if(emailUser):
			flash('That email address is already registered for another user, please enter a different email.', 'alert-danger')
		if(usernameUser):
			flash('That username is already in user, please enter a different username.', 'alert-danger')
		if(not usernameUser and not emailUser):
			user = User(username=form.username.data, name=form.name.data, password=form.password.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
			flash('Registration successful!', 'alert-success')

			token = generate_email_confirmation_token(user.email)
			msg = Message('Confirm Email', sender = 'FlaskCMT120@gmail.com', recipients=[user.email])
			msg.html = render_template('emails/email-confirm-email.html', user=user, token=token)
			mail.send(msg)
			flash('You will receive an email to activate your account shortly', 'alert-info')

			return redirect(url_for('registered'))
	return render_template('register.html', title='register', form=form)

@app.route("/registered")
def registered():
	return render_template('registered.html', title='Thanks!')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if (user != None and user.verify_password(password=form.password.data) and user.confirmed):

			if user.mfa_enabled:
				return redirect(url_for('login_mfa', user_id=user.id))
			else:
				user.login_count = user.login_count + 1
				user.active = True
				user.current_login_at = datetime.now()
				db.session.add(user)
				db.session.commit()
				login_user(user)
				flash('Login successful', 'alert-success')
				return redirect(url_for('home'))
		else:
			flash('This account has not been confirmed or the password you entered was incorrect, please try again', 'alert-danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/login/mfa/<int:user_id>", methods=['GET', 'POST'])
def login_mfa(user_id):
	user = User.query.filter_by(id=user_id).first()
	form = MFAForm()
	if form.validate_on_submit():
		if user.verify_totp(form.otp.data) and form.otp.data != user.last_used_code:
			login_user(user)
			user.last_used_code = form.otp.data
			user.login_count = user.login_count + 1
			user.active = True
			user.current_login_at = datetime.now()
			db.session.add(user)
			db.session.commit()
			flash('Login successful', 'alert-success')
			return redirect(url_for('home'))
		else:
			flash('Incorrect OTP, please try again', 'alert-danger')
	return render_template('login-mfa.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
	user = User.query.filter_by(id=current_user.id).first()
	user.active = False
	user.last_login_at = datetime.now()
	user.current_login_at = None
	db.session.add(user)
	db.session.commit()
	logout_user()
	flash('You have logged out of your account', 'alert-info')
	return redirect(url_for('home'))

@app.route("/user-dashboard")
@login_required
def user_dashboard():
	return render_template('user-dashboard.html')

@app.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
	form=ChangePasswordForm()
	if form.validate_on_submit():
		if (current_user.verify_password(password=form.oldPassword.data)):
			current_user.password = form.newPassword.data
			db.session.add(current_user)
			db.session.commit()
			flash('Your password has been changed', 'alert-success')
			return redirect(url_for('user_dashboard'))
		else:
			flash('Incorrect password, please try again', 'alert-danger')
	return render_template('change-password.html', form=form)

@app.route("/update-details", methods=['GET', 'POST'])
@login_required
def update_details():
	form=UpdateDetailsForm()
	form.username.data = current_user.username
	form.name.data = current_user.name
	if form.validate_on_submit():
		usernameUser = User.query.filter(User.id != current_user.id).filter_by(username=form.username.data).first()
		if(usernameUser):
			flash('That username is already in user, please enter a different username.', 'alert-danger')
		else:
			current_user.username = form.username.data
			current_user.name = form.name.data			
			db.session.add(current_user)
			db.session.commit()
			flash('Your details have been changed', 'alert-success')
			return redirect(url_for('user_dashboard'))
	return render_template('update-details.html', form=form)

# Individual db object pages

@app.route("/project/<int:project_id>", methods=['GET', 'POST'])
def project(project_id):
	project = Projects.query.get_or_404(project_id)
	skills = db.session.query(Skills).join(SkillsToProjects, Skills.id==SkillsToProjects.skill_id).filter(SkillsToProjects.project_id==project_id).all()
	#returns a list of skills linked to the project using SkillsToProjects table
	commentForm = CommentForm()
	ratingForm = RatingForm()
	comments = Comments.query.filter(Comments.page == 'project', Comments.page_id == project_id).order_by(Comments.comment_time.asc()).all()
	ratingsList = Ratings.query.filter(Ratings.page == 'project', Ratings.page_id == project_id).all()
	if ratingsList:
		overallRating = round(sum(rating.rating for rating in ratingsList) / len(ratingsList), 2)
	else:
		overallRating = 0
	# if else to prevent division by 0
	if commentForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to add a comment', 'alert-info')
			return redirect(url_for('login')) 
		addComment(commentForm, 'project', project_id)
		return redirect(url_for('project', project_id = project_id))
	if ratingForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to submit a rating', 'alert-info')
			return redirect(url_for('login')) 
		addRating(ratingForm, 'project', project_id)
		return redirect(url_for('project', project_id = project_id))
	return render_template('project.html', title=project.title, project=project, skills=skills, commentForm=commentForm, ratingForm=ratingForm, comments=comments, rating=overallRating)

@app.route("/work/<int:work_id>", methods=['GET', 'POST'])
def work(work_id):
	work = Work.query.get_or_404(work_id)
	commentForm = CommentForm()
	ratingForm = RatingForm()
	comments = Comments.query.filter(Comments.page == 'work', Comments.page_id == work_id).order_by(Comments.comment_time.asc()).all()
	ratingsList = Ratings.query.filter(Ratings.page == 'work', Comments.page_id == work_id).all()
	if ratingsList:
		overallRating = round(sum(rating.rating for rating in ratingsList) / len(ratingsList), 2)
	else:
		overallRating = 0
	# if else to prevent division by 0
	if commentForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to add a comment', 'alert-info')
			return redirect(url_for('login')) 
		addComment(commentForm, 'work', work_id)
		return redirect(url_for('work', work_id=work_id))

	if ratingForm.validate_on_submit():
		if not current_user.is_authenticated:
			flash('You must be logged in to submit a rating', 'alert-info')
			return redirect(url_for('login')) 
		addRating(ratingForm, 'work')
		return redirect(url_for('work', work_id=work_id))

	return render_template('work.html', title=work.job_title, work=work, commentForm=commentForm, ratingForm=ratingForm, comments=comments, rating=overallRating)

#Account management pages

@app.route("/forgot-password", methods=['GET', 'POST'])
def forgot_password():
	form=ForgotForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			token = generate_password_confirmation_token(user.hashed_password)
			msg = Message('Password Reset', sender = 'FlaskCMT120@gmail.com', recipients=[user.email])
			msg.html = render_template('emails/email-forgot-password.html', user=user, token=token)
			mail.send(msg)
		#indent so malicious user does not know if they have correctly identified a user account
		flash('You will receive a password reset email shortly', 'alert-info')
		return redirect(url_for('home'))
	return render_template('forgot-password.html', form=form)

@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password(token):
	try:
		hashed_password = confirm_password_token(token)
	except:
		flash('The reset link is invalid or has expired.', 'alert-danger')
		return redirect(url_for('home'))
	user = User.query.filter_by(hashed_password=hashed_password).first_or_404()
	form = PasswordRecoveryForm()
	if form.validate_on_submit():
		user.password = form.password.data
		db.session.add(user)
		db.session.commit()
		flash('Password updated successfully', 'alert-success')
		return redirect(url_for('home'))
	return render_template('reset-password.html', form=form)

@app.route("/confirm-email/<token>")
def confirm_email(token):
	try:
		email = confirm_email_token(token)
	except:
		flash('The confirmation link is invalid or has expired.', 'alert-danger')
		return redirect(url_for('login'))

	user = User.query.filter_by(email=email).first_or_404()
	if user.confirmed:
		flash('Account already confirmed. Please login.', 'alert-info')
	else:
		user.confirmed = True
		user.confirmed_at = datetime.now()
		db.session.add(user)
		db.session.commit()
		flash('You have confirmed your account. Thanks!', 'alert-success')
	return redirect(url_for('login'))

@app.route("/setup-mfa")
@login_required
def setup_mfa():
	if current_user.mfa_enabled:
		flash('MFA is already enabled for your account', 'alert-info')
		return redirect(url_for('home'))
	user = User.query.filter_by(id=current_user.id).first_or_404()
	user.mfa_enabled = True
	user.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
	uri = pyotp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='FLASK-CMT120')

	db.session.add(user)
	db.session.commit()
	
	return render_template('setup-mfa.html', uri=uri), {
		'Cache-Control':'no-cache, no-store, must-revalidate',
		'Pragma':'no-cache',
		'Expires':'0'
	}
	#added code to prevent caching of the QR code setup

@app.route("/qr-code")
@login_required
def qr_code():
	user = User.query.filter_by(id=current_user.id).first_or_404()
	user.mfa_enabled = True
	user.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
	uri = pyotp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='FLASK-CMT120')
	return uri

@app.route("/disable-mfa", methods=['GET', 'POST'])
@login_required
def disable_mfa():
	if not current_user.mfa_enabled:
		flash('MFA is not yet enabled for your account', 'alert-info')
		return redirect(url_for('user_dashboard'))
	form = VerifyPasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(password=form.password.data):
			return redirect(url_for('disable_mfa_confirm'))
		else:
			flash('Incorrect Password', 'alert-danger')
	return render_template('disable-mfa.html', form=form)

@app.route("/disable-mfa-confirm", methods=['GET', 'POST'])
@login_required
def disable_mfa_confirm():
	form=MFAForm()
	if form.validate_on_submit():
		if current_user.verify_totp(form.otp.data) and form.otp.data != current_user.last_used_code:
			current_user.mfa_enabled = False
			current_user.otp_secret = None
			current_user.last_used_code = None
			db.session.add(current_user)
			db.session.commit()
			flash('MFA has been disabled for your account', 'alert-info')
			return redirect(url_for('user_dashboard'))
	return render_template('disable-mfa-confirm.html', form=form)

# Error Pages
@app.errorhandler(401)
def page_not_found(e):
	flash('You do not currently have access to this page. Please login to an account with access priviledges and try again.', 'alert-danger')
	return redirect(url_for('login')), 401

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500
