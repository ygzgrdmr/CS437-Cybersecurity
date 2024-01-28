from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500))
    link = db.Column(db.String(300))
    uploaded_by = db.Column(db.String(100))  # If it's a user-uploaded article

    def __repr__(self):
        return f"<Article {self.title}>"
