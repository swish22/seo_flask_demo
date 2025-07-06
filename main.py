from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import git

#handle redirects
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '76195a107bcc4e72a1b43ac4cd5dca66'


# webpage

# base page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title ='Home Page', subtitle='Welcome!', text='This is the home page')


# form page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

# about page
@app.route("/about")
def about():
    return render_template('about.html', title ='About Page', subtitle='Learn about this site!', text='This is the about page')

# auto-update logic
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/swish22/mysite/seo_flask_demo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
  app.run(debug=True, host ="0.0.0.0")
