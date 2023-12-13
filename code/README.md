# c22076087_cmt120_cw2

## Name 

Flask CMT120 Project

Username: c22076087
Proejct Link: http://c-22076087-cmt-120-cw-2-git-flask-cmt120-c22076087.apps.openshift.cs.cf.ac.uk/

## Description

This is my CMT120 Assessment 2 Flask Project, designed for my Cardiff University MSc Computing course.

Requirements for this project are listed in the requirements.txt file

The final code is authored by myself, with references given below where code has been taken from or inspired by other projects and tutorials. Images are all open source and referenced as part of the website. 

This project has been submitted for assessment and no further changes are expected after 22/01/2023

## Using the project

To log in as an administrator, use the following details

Username: adminuser
Password: J@H\o7ek@A<7.KU^zmE%p~R4E'am}hp\

This will automatically reveal a navbar with which to access flask admin. Please do not update the administrator password for other users. If you wish to make your own account an administrator that can be done via editing the admin field in the User page on the flask admin page.

Functionality for image uploading and deleting may not be working due to a lack of access control over app permissions to write files onto the Openshift box. However if a user wanted to test these they could clone locally and run on their own machine so long as their application had permission to write to the blog/static/img directory. 

## Functionality
*	Login system
*	Password hashing
*	Confirmation email with expiry
*	Account confirmation via email token
*	Account recovery via password reset email
*	Password changing through website
*	Updating user details through website
*	2 Factor Authentication for user
*	QR code to share 2FA secret
*	API call to tell a programming joke
*	Comment system
*	Comments styled individually using javascript
*	Rating system, allowing only one rating per user
*	Database maintenance through Flask Admin
*	Custom validations through Flask Admin
*	Hiding of fields and disabling of adding rows for Users
*	User admin validation on Flask Admin pages
*	Uploading and deleting images through custom Flask Admin page
*	Custom links in Flask Admin navbar 
*	Bootstrap5 stylings across the whole site
*	Alert system for events
*	Password strength indicator through javascript
*	Custom error pages

## References

In addition to the below references, I made use of an API at https://official-joke-api.appspot.com/jokes/programming/random in order to tell the user a random programming joke on the user dashboard.

akshaysingh98088, mishrapriyank17, (Geeks For Geeks). 2021. How to create a progress bar in different colors in Bootstrap ? [Code Guide] Available at: https://www.geeksforgeeks.org/how-to-create-a-progress-bar-in-different-colors-in-bootstrap/ [Accessed: 15 January 2023]

baddy12, surajkr_gupta, (Geeks For Geeks). 2022. Get current date using Python. [Code Guide]. Available at: https://www.geeksforgeeks.org/get-current-date-using-python/ [Accessed: 16 January 2023]

Dag Wieers, davidism, stackoverflow users. 2019. String concatenation in Jinja [Code Q and A]. Available at: https://stackoverflow.com/questions/2061439/string-concatenation-in-jinja#:~:text=You%20can%20use%20%2B%20if%20you%20know%20all,my_string%20%3D%20my_string%20~%20stuff%20~%20%27%2C%20%27%25%7D [Accessed: 19 January 2023]

Elder, J. Codemy.com. 2021. Custom Error Pages and Version Control - Flask Fridays #3. [Code Guide] Available at: https://www.youtube.com/watch?v=3O4ZmH5aolg&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=4 [Accessed: 7 January 2023]

Elder, J, Codemy.com. 2021. Delete Database Records With Flask - Flask Fridays #12. [Code Guide] Available at: https://www.youtube.com/watch?v=7jKsHOZk-IE&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=13 [Accessed: 9 January 2023]

Elder, J, Codemy.com. 2021. Edit Blog Posts - Flask Fridays #20. [Code Guide] Available at: https://www.youtube.com/watch?v=N4Nz0cYuCnc&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=22 [Accessed: 6 January 2023]

Elder, J, Codemy.com. 2021. Fix And Show Profile Picture - Flask Fridays #41
. [Code Guide] Available at: https://www.youtube.com/watch?v=CDDWZE0n7Mk&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=42 [Accessed: 12 January 2023]

Elder, J, Codemy.com. 2021. Upload Profile Picture - Flask Fridays #38. [Code Guide] Available at: https://www.youtube.com/watch?v=ZHQtxITPcAs&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=39 [Accessed: 12 January 2023]

Elder, J, Codemy.com. 2021. User Login with Flask_Login - Flask Fridays #22. [Code Guide] Available at: https://www.youtube.com/watch?v=bxyaJ8w_wak&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=23 [Accessed: 10 January 2023]

Fast Web Start. 2023. Set Background Image for a div [Code Guide]. Available at: http://fastwebstart.com/html-div-background-image/#:~:text=In%20order%20to%20add%20a%20background%20image%20to,image%20%E2%80%9Ccute-baby.jpg%E2%80%9D.%20You%20can%20add%20it%20as%20follows%3A [Accessed: 20 January 2023]

Flask. 2010. Message Flashing. [Code Documentation]. Available at: https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/ [Accessed: 18 January 2023]

Flask Admin. 2019. flask_admin.base API. [Code Documentation] Available at: https://flask-admin.readthedocs.io/en/latest/api/mod_base/ [Accessed: 16 January 2023]

Flask Admin. 2019. flask_admin.form.upload API. [Code Documentation] Available at: https://flask-admin.readthedocs.io/en/latest/api/mod_form_upload/ [Accessed: 12 January 2023]

Flask Admin. 2019. flask_admin.model API. [Code Documentation] Available at: https://flask-admin.readthedocs.io/en/latest/api/mod_model/ [Accessed: 12 January 2023]

Flask Admin. 2019. Introduction To Flask-Admin. [Code Documentation] Available at: https://flask-admin.readthedocs.io/en/latest/introduction/ [Accessed: 12 January 2023]

Grinberg, M. 2015. Two Factor Authentication with Flask. [Code Guide] Available at: https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask [Accessed: 14 January 2023]

herald jose, stackoverflow user. 2021. Flask email link prefixed with link [Code Q and A]. Available at: https://stackoverflow.com/questions/63498127/flask-email-link-prefixed-with-link [Accessed: 13 January 2023]

MDN. 2022. HTMLElement: input event. [Code Guide]. Available at: https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event [Accessed: 15 January 2023]

mritunjays8630, sagartomar9927, (Geeks For Geeks). 2022. Bootstrap 5 Figures. [Code Guide]. Available at: https://www.geeksforgeeks.org/bootstrap-5-figures/ [Accessed: 21 January 2023]

NeuralNine. 2022. Two-Factor Authentication (2FA) in Python. [Code Guide] Available at: https://www.youtube.com/watch?v=o0XZZkI69E8 [Accessed: 14 January 2023]

phihag, stackoverflow user. 2012. Sum / Average an attribute of a list of objects [Code Q and A]. Available at: https://stackoverflow.com/questions/10879867/sum-average-an-attribute-of-a-list-of-objects [Accessed: 11 January 2023]

Pretty Printed. 2016. Intro to Flask-Admin. [Code Guide] Available at: https://www.youtube.com/watch?v=ysdShEL1HMM [Accessed: 12 January 2023]

pyotp. 2022. Python One Time Password Library. [Code Documentation] Available at: https://pypi.org/project/pyotp/ [Accessed: 14 January 2023]
Real Python. 2015. Handling Email Confirmation During Registration in Flask. [Code Guide] Available at: https://realpython.com/handling-email-confirmation-in-flask/ [Accessed: 13 January 2023]

Serban Razvan, stackoverflow user. 2013. How to use "/" (directory separator) in both Linux and Windows in Python? [Code Q and A]. Available at: https://stackoverflow.com/questions/16010992/how-to-use-directory-separator-in-both-linux-and-windows-in-python [Accessed: 22 January 2023]

SQLAlchemy. 2021. SQLAlchemy 1.3 Documentation. [Code Guide]. Available at: https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter [Accessed: 6 January 2023]

tanishkagupta1 (Geeks For Geeks). 2019. Email Template using HTML and CSS. [Code Template] Available at: https://www.geeksforgeeks.org/email-template-using-html-and-css/ [Accessed: 13 January 2023]

Toh W. S. (Code Boxx). 2022. 3 Ways to Keep Image Aspect Ratio In HTML CSS [Code Guide]. Available at: https://code-boxx.com/keep-image-aspect-ratio/#:~:text=To%20maintain%20the%20aspect%20ratio%20of%20images%20in,%7D%20img.demoB%20%7B%20width%3A%20auto%3B%20height%3A%20600px%3B%20%7D [Accessed: 20 January 2023]

user559633, stackoverflow user. 2014. Add a css class to a field in wtform [Code Q and A]. Available at: https://stackoverflow.com/questions/22084886/add-a-css-class-to-a-field-in-wtform [Accessed: 9 January 2023]

Web Tech Survey. 2022. Bootstrap. [Web Survey]. Available at: https://webtechsurvey.com/technology/bootstrap [Accessed: 20 January 2023]

WTForms. 2008. Fields [Code Documentation]. Available at: https://wtforms.readthedocs.io/en/2.3.x/fields/ [Accessed: 11 January 2023]

W3 Docs. 2018. How to Add an HTML Button that Acts Like a Link
. [Code Guide] Available at: https://www.w3docs.com/snippets/html/how-to-create-an-html-button-that-acts-like-a-link.html [Accessed: 9 January 2023]

W3 Schools. 2023. Bootstrap 5 Alerts. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_alerts.php [Accessed: 9 January 2023]

W3 Schools. 2023. Bootstrap 5 Background Colors. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_colors_bg.php [Accessed: 17 January 2023]

W3 Schools. 2023. Bootstrap 5 Button Groups. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_button_groups.php [Accessed: 10 January 2023]

W3 Schools. 2023. Bootstrap 5 Cards. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_cards.php [Accessed: 17 January 2023]

W3 Schools. 2023. Bootstrap 5 Get Started. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_get_started.php [Accessed: 5 January 2023]

W3 Schools. 2023. Bootstrap 5 Images. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_images.php [Accessed: 17 January 2023]

W3 Schools. 2023. Bootstrap 5 List Groups. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_list_groups.php [Accessed: 17 January 2023]

W3 Schools. 2023. Bootstrap 5 Navbars. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_navbar.php [Accessed: 8 January 2023]

W3 Schools. 2023. Bootstrap Progress Bars. [Code Guide]. Available at: https://www.w3schools.com/bootstrap/bootstrap_progressbars.asp [Accessed: 15 January 2023]

W3 Schools. 2023. Bootstrap 5 Text/Typography. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_typography.php  [Accessed: 17 January 2023]

W3 Schools. 2023. Bootstrap 5 Utilities. [Code Guide]. Available at: https://www.w3schools.com/bootstrap5/bootstrap_utilities.php [Accessed: 17 January 2023]

W3 Schools. 2023. How TO - Range Sliders. [Code Guide]. Available at: https://www.w3schools.com/howto/howto_js_rangeslider.asp [Accessed: 11 January 2023]

W3 Schools. 2023. JavaScript Switch Statement. [Code Guide]. Available at: https://www.w3schools.com/js/js_switch.asp [Accessed: 15 January 2023]

W3 Schools. 2023. Python RegEx. [Code Guide]. Available at: https://www.w3schools.com/python/python_regex.asp [Accessed: 5 January 2023]
