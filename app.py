from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
oauth = OAuth(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Configure OAuth
oauth.register(
    name='identity-management',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    authorize_url='http://identity-management-app:5000/oauth/authorize',
    authorize_params=None,
    access_token_url='http://identity-management-app:5000/oauth/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://webova-app:5000/auth',
    client_kwargs={'scope': 'openid profile email'}
)

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, session['name'])

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return oauth.identity_management.authorize_redirect(redirect_uri='http://webova-app:5000/auth')

@app.route('/auth')
def auth():
    token = oauth.identity_management.authorize_access_token()
    user_info = oauth.identity_management.parse_id_token(token)
    user = User(user_info['sub'], user_info['name'])
    login_user(user)
    return redirect(url_for('green'))

@app.route('/green')
def green():
    return render_template('green.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)