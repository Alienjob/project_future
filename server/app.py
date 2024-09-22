from flask import Flask, render_template, url_for
from flask_login import current_user
from extensions import db, login_manager
from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Import and register blueprints
from auth import auth as auth_blueprint
from tasks import tasks as tasks_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(tasks_blueprint)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)