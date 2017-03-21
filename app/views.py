"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from form import LoginForm, ProfileForm
from models import UserProfile
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
import os, time, json, random
from werkzeug.utils import secure_filename
import uuid

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
#@login_required
def profileform ():
    form = ProfileForm() 
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        age = request.form['age']
        biography = request.form['biography']
        
        file_folder = app.config["UPLOAD_FOLDER"]
        image = request.files['image']
        imageName = secure_filename(image.filename)
        image.save(os.path.join(file_folder, imageName))
        
        while True:
            userid = random.randint(6000000,6999999) #Generates a random id for the user
            userid_data = UserProfile.query.filter_by(userid=userid).first()
            if userid_data is None:
                #Genereated userid is unique
                break
        gender = request.form['gender']
        created_on = timeinfo()
        profile = UserProfile(userid,first_name,last_name,username,age,biography,imageName,gender,created_on)
        db.session.add(profile)
        db.session.commit()
        flash("Your Profile has been created!! User Successfully Added!", category = 'success')
        return redirect (url_for('allprofilesform'))
    return render_template('profile.html',form=form)
    


        
@app.route('/profiles', methods= ['GET','POST'])
#@login_required
def allprofilesform ():
    users = db.session.query(UserProfile).all()
    if request.headers.get('content-type') == 'application/json' and request.method == 'POST':
        allusers=[]
        for user in users:
            pro={'username':user.username,'userid':str(user.userid)}
            allusers.append(pro)
        return jsonify(users = allusers)
    else:
        if not users:
            flash('There are no users in the Application Database')
            return redirect(url_for('profileform'))
        return render_template('profiles.html', users=users)
        

@app.route('/profile/<userid>', methods= ['GET','POST'])
#@login_required
def personalprofileform (userid):
    user= db.session.query(UserProfile).filter_by(userid=userid).first()
    if request.headers.get('content-type') == 'application/json' and request.method == 'POST':
        if user:
            return jsonify({'userid': str(user.userid),'username':user.username, 'image':user.image,'gender':user.gender,'age':str(user.age),'profile_created_on':user.created_on})
        else:
            return jsonify(user)
    else:
        if not user:
            flash('User does not exist.','danger')
            return redirect(url_for('allprofilesform'))
        else:
            return render_template('personalprofile.html', user = user)
    
        
def timeinfo():
	date = time.strftime("%d %b %Y")

	return date
	
	
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserLogin.query.get(int(id))

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