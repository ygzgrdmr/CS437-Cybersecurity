from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_apscheduler import APScheduler
from routes import init_routes
from func import fetch_rss_feeds
from models import User, db
from database import db, Article

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy with the Flask app
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

class Config(object):
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# Function to fetch and update feeds
def update_feeds():
    with app.app_context():
        feeds = fetch_rss_feeds()  # your function to fetch feeds
        for feed in feeds:
            article = Article(title=feed['title'], summary=feed['summary'], link=feed['link'])
            db.session.add(article)
        db.session.commit()

# Schedule the 'update_feeds' to run every 30 minutes
scheduler.add_job(id='Scheduled Task', func=update_feeds, trigger='interval', minutes=30)

# Initialize routes
init_routes(app, cache)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables based on models
    app.run(debug=True)
