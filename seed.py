# seeds the database with sample users, lessons, and progress
from models import db, User, Lesson, UserProgress
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json, os

from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    # create sample users
    u1 = User(username="alice", password_hash=generate_password_hash("password123"))
    u2 = User(username="bob", password_hash=generate_password_hash("secret"))
    db.session.add_all([u1,u2])
    db.session.commit()

    # create sample lessons
    lessons = [
        {
            "title":"Intro to Microlearning",
            "content":"Microlearning delivers content in small, focused chunks. Learn quickly!",
            "quiz":[
                {"question":"Microlearning content should be ...?","options":["Long","Short","Irrelevant"],"answer":"Short"}
            ]
        },
        {
            "title":"Effective Study Tips",
            "content":"Use spaced repetition, active recall, and short focused sessions.",
            "quiz":[
                {"question":"Which is a study technique?","options":["Spaced repetition","Cramming forever","Never review"],"answer":"Spaced repetition"}
            ]
        },
        {
            "title":"Quick Python Basics",
            "content":"Variables, loops, and functions are core concepts in Python.",
            "quiz":[
                {"question":"Which keyword defines a function in Python?","options":["func","def","function"],"answer":"def"}
            ]
        }
    ]
    for ls in lessons:
        l = Lesson(title=ls["title"], content=ls["content"], quiz_json=json.dumps(ls["quiz"]))
        db.session.add(l)
    db.session.commit()

    # add some progress for Alice: two lessons, yesterday and today
    now = datetime.utcnow()
    db.session.add(UserProgress(user_id=1, lesson_id=1, timestamp=now - timedelta(days=1)))
    db.session.add(UserProgress(user_id=1, lesson_id=2, timestamp=now))
    db.session.commit()
    print("Seeded database: users, lessons, progress")
