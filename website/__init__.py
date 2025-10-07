import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


DB_NAME = 'database.db'
db = SQLAlchemy()




def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    # Build absolute DB path in project root (one level above website/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, DB_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    from .models import User , Book,Borrow
    create_database(app, db_path)
    
    from .views import views
    from .auth import auth
    from .api import api


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')


      # Set up LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app, db_path):
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            seed_data()
        print(f' Database created at: {db_path}')
    else:
        print(f' Database already exists at: {db_path}')


def seed_data():
# Create a default admin and some books
 from .models import User, Book
 from werkzeug.security import generate_password_hash
 admin = User(name='Admin', email='admin@example.com', password=generate_password_hash('admin123'), is_admin=True)
 user = User(name='Maram', email='maram@example.com', password=generate_password_hash('password'))
 db.session.add_all([admin, user])
 b1 = Book(title='Clean Code', author='Robert C. Martin', description='A Handbook of Agile Software Craftsmanship', stock=3)
 b2 = Book(title='Deep Learning', author='Ian Goodfellow', description='An MIT Press Book', stock=2)
 b3 = Book(title='Introduction to Algorithms', author='Cormen, Leiserson, Rivest, Stein', description='Classic algorithms textbook', stock=1)
 db.session.add_all([b1, b2, b3])
 db.session.commit()
 print('Seeded database with default users and books')
 