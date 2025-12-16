from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your-secret-key"

# ---------------------------
# MongoDB CONNECTION
# ---------------------------
MONGO_URI = "mongodb+srv://ariyask2006_db_user:ariyask2006@cluster0.xv08dev.mongodb.net/"  # change if using MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["sk_diary"]
entries = db.entries

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    i_call_you = request.form.get("i_call_you")
    ring_me_at = request.form.get("ring_me_at")
    birthday = request.form.get("birthday")
    one_day = request.form.get("one_day")
    best_memory = request.form.get("best_memory")

    uploaded_files = []
    if "photos" in request.files:
        files = request.files.getlist("photos")
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
                filename = f"{timestamp}_{filename}"
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                f.save(path)
                uploaded_files.append(path)

    record = {
        "first_name": first_name,
        "last_name": last_name,
        "i_call_you": i_call_you,
        "ring_me_at": ring_me_at,
        "birthday": birthday,
        "one_day": one_day,
        "best_memory": best_memory,
        "photos": uploaded_files,
        "submitted_at": datetime.utcnow()
    }

    entries.insert_one(record)
    flash("Your entry was saved!", "success")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
