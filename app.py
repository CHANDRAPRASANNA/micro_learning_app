from flask import Flask, jsonify, request, g
from flask_cors import CORS
from models import db, User, Lesson, UserProgress, Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error":"Missing Authorization header"}), 401
        s = Session.query.filter_by(token=token).first()
        if not s:
            return jsonify({"error":"Invalid token"}), 401
        g.current_user = User.query.get(s.user_id)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error":"username and password required"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error":"username taken"}), 400
    u = User(username=data["username"], password_hash=generate_password_hash(data["password"]))
    db.session.add(u); db.session.commit()
    return jsonify({"message":"registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    u = User.query.filter_by(username=data.get("username")).first()
    if not u or not check_password_hash(u.password_hash, data.get("password","")):
        return jsonify({"error":"invalid credentials"}), 401
    token = str(uuid.uuid4())
    s = Session(user_id=u.id, token=token, created_at=datetime.utcnow())
    db.session.add(s); db.session.commit()
    return jsonify({"token":token, "user_id": u.id, "username": u.username})

@app.route("/lessons", methods=["GET"])
@token_required
def get_lessons():
    lessons = Lesson.query.all()
    out = []
    for lesson in lessons:
        out.append({
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "quiz": json.loads(lesson.quiz_json)
        })
    return jsonify(out)

@app.route("/lesson/<int:id>", methods=["GET"])
@token_required
def get_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    return jsonify({
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "quiz": json.loads(lesson.quiz_json)
    })

@app.route("/progress", methods=["POST"])
@token_required
def save_progress():
    data = request.json
    user = g.current_user
    lesson_id = data.get("lesson_id")
    completed = data.get("completed", True)
    # avoid duplicate entry for same day
    entry = UserProgress(user_id=user.id, lesson_id=lesson_id, timestamp=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message":"progress saved"})

@app.route("/progress/<int:user_id>", methods=["GET"])
@token_required
def get_progress(user_id):
    progress = UserProgress.query.filter_by(user_id=user_id).all()
    completed = [{"lesson_id":p.lesson_id, "timestamp":p.timestamp.isoformat()} for p in progress]
    return jsonify({"completed": completed})

@app.route("/leaderboard", methods=["GET"])
@token_required
def leaderboard():
    # simple: rank users by count of distinct lessons completed
    users = User.query.all()
    board = []
    for u in users:
        c = db.session.query(UserProgress.lesson_id).filter_by(user_id=u.id).distinct().count()
        board.append({"user_id":u.id, "username":u.username, "completed_lessons": c})
    board = sorted(board, key=lambda x: x["completed_lessons"], reverse=True)
    return jsonify(board)

@app.route("/streak/<int:user_id>", methods=["GET"])
@token_required
def streak(user_id):
    # compute current daily streak: count of consecutive days with at least one completion
    from sqlalchemy import func
    rows = db.session.query(func.date(UserProgress.timestamp)).filter_by(user_id=user_id).distinct().order_by(UserProgress.timestamp.desc()).all()
    days = [r[0] for r in rows]
    if not days:
        return jsonify({"streak":0})
    # days are strings 'YYYY-MM-DD' ordered desc
    streak = 0
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    cur = today
    for d in days:
        dd = datetime.strptime(d, "%Y-%m-%d").date()
        if dd == cur:
            streak += 1
            cur = cur - timedelta(days=1)
        elif dd < cur:
            break
    return jsonify({"streak":streak})

if __name__ == "__main__":
    import json
    app.run(debug=True)
