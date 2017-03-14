"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import uuid
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from form import LoginForm
from models import UserProfile
from app import app
from flask import render_template, request, redirect, url_for, flash
from .form import ProfileForm
import time
import os
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("secure_page"))
    
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = UserProfile.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user)
            # get user id, load into session
            flash('Logged in successfully.', 'success')
            # remember to flash a message to the user
            return redirect(url_for("secure_page")) # they should be redirected to a secure-page route instead
        else:
            flash("Username or password is incorrect")
            #return redirect(url_for("login"))
    flash_errors(form)
    return render_template("login.html", form=form)
    
    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))
    
@app.route("/secure-page")
@login_required
def secure_page():
    return render_template("secure_page.html")
    

@app.route('/profile', methods= ['GET','POST'])
def profileform ():
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            """post method filler"""
            username = request.form['username']
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            age = request.form['age']
            biography = request.form['biography']
            image = request.form['image']
            gender = request.form['gender']
            created_on = timeinfo()
            userid = uuid.uuid4()
            
            if image and allowed_file(image.filename):
            pic = secure_filename(image.filename)
            path ="/static/uploads/"+ pic
            image.save("./app"+path)
            image =path
            prof = UserProfiles(1,firstname,lastname,username,gender,age,bio,image,date())
            db.session.add(prof)
            db.session.commit()
            return redirect (url_for('home'))
    return render_template('profile.html',form=pform)
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

        
@app.route('/profiles', methods= ['GET','POST'])
def allprofilesform ():
    form = AllProfilesForm()
    users=[]
    xl=[]
    p={}
    i=0
    print request.method
    if request.method=="POST":
        users= db.session.query(UserProfile).all()
        for user in users:
            p={'username':user.username,'userid':str(user.id)}
            users.insert(i,p)
            i+=1
        x={'users':jsonify(users)}
        xl.insert(0,x)
        print x
        # return jsonify(x)
        return jsonify(users)
    users   = db.session.query(UserProfile).all()
    for user in users:
        users.append((user.firstname, user.username))
    return render_template('profiles.html',users=users)
        


@app.route('/profile/<userid>', methods= ['GET','POST'])
def personalprofileform (userid):
    form = PersonalProfileForm()
    user={}
    i=0
    if request.method=='POST':
        users= db.session.query(UserProfile).filter_by(username=userid)
        for user in users:
            p={'userid':str(user.id),'username':user.username, 'image':user.profpic,'gender':user.gender,'age':str(user.age),'profile_created_on':user.date_created}
            # user.insert(i,p)
            i+=1
        return jsonify(p)
    users= db.session.query(UserProfile).filter_by(username=userid)
    return render_template('viewprof.html',users=users)
        
def timeinfo():
	date = time.strftime("%d %b %Y")

	return date
	
	
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")