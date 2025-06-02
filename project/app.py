from flask import Flask, render_template, request, session, redirect, url_for, flash
from project.models.user import User, Content
from .detectors import analyze_content, get_high_risk_contents, get_spread_map, record_spread
from collections import defaultdict
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key'


users = {}
contents = {}
known_checksums = set()


if not users:
    users["1"] = User("1", "pandii", "tester@example.com")

TEXTS = {
    "en": {
        "users": "users",
        "uploads": "uploads",
        "flagged": "flagged",
        "tip": "Always verify content authenticity before sharing.",
        "need_help": "Need Help?"
    },
    "id": {
        "users": "pengguna",
        "uploads": "unggahan",
        "flagged": "ditandai",
        "tip": "Selalu periksa keaslian konten sebelum membagikan.",
        "need_help": "Butuh Bantuan?"
    }
}

@app.route("/")
def index():
    lang = session.get("lang", "en")
    texts = TEXTS[lang]
    stats = {
        "users": len(users),
        "uploads": len(contents),
        "flagged": len(get_high_risk_contents())
    }
    return render_template("index.html", session=session, stats=stats, texts=texts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        if email == "admin@example.com":
            username = "admin"
            role = "admin"
        else:
            username = request.form["username"]
            role = "user"

        user_id = str(len(users) + 1)
        users[user_id] = User(user_id, username, email)
        session["username"] = username
        session["user_id"] = user_id
        session["role"] = role  # ⬅ SIMPAN role di session
        session["toast"] = "Registration successful!"
        return redirect("/")
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        for uid, user in users.items():
            if user.username == username:
                session["username"] = username
                session["user_id"] = uid
                session["role"] = "admin" if username == "admin" else "user" 
                session["toast"] = "Welcome back!"
                return redirect("/")
        return render_template("login.html", error="User not found")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/upload-form", methods=["GET", "POST"])
def upload_form():
    if "username" not in session:
        return redirect("/login")

    if session.get("username") == "admin":
        session["toast"] = "Admin tidak diizinkan mengunggah konten."
        return redirect("/")

    if request.method == "POST":
        user_id = request.form.get("user_id")
        if user_id not in users:
            flash("User tidak ditemukan.")
            return redirect("/upload-form")

        filename = request.form.get("filename")
        metadata = {
            "camera": request.form.get("camera"),
            "ai-engine": request.form.get("ai_engine"),
            "resolution": request.form.get("resolution"),
            "x-fake-score": float(request.form.get("x_fake_score", 0))
        }

        content = Content(users[user_id], filename, metadata)
        result = analyze_content(content, known_checksums)

        contents[content.content_id] = content
        known_checksums.add(content.checksum)
        record_spread(content.uploader, content)

        session["toast"] = "Upload processed."
        return redirect("/spread-map")

    return render_template("upload_form.html", users=users)

@app.route("/admin/dashboard")
def admin_dashboard():
    if "username" not in session or session["username"] != "admin":
        return redirect("/login")

    total_users = len(users)
    total_contents = len(contents)
    risk_items = get_high_risk_contents()
    total_risk = len(risk_items)

    safe_count = total_contents - total_risk

    # Count uploads per user
    uploads_per_user = defaultdict(int)
    for content in contents.values():
        uploads_per_user[content.uploader.username] += 1

    return render_template("admin_dashboard.html",
                           total_users=total_users,
                           total_contents=total_contents,
                           total_risk=total_risk,
                           safe_count=safe_count,
                           uploads_per_user=dict(uploads_per_user))

@app.route("/admin/only")
def admin_only():
    if session.get("username") != "admin":
        return redirect("/")
    return render_template("admin_only.html")


@app.route("/content/<content_id>")
def content_detail(content_id):
    if "username" not in session:
        return redirect("/login")
    
    content = contents.get(content_id)
    if not content:
        return "Content not found", 404

    return render_template("content_detail.html", content=content)


@app.route("/high-risk")
def high_risk():
    if "username" not in session:
        return redirect("/login")

    grouped = defaultdict(list)
    for item in get_high_risk_contents():
        user = item["content"].uploader.username
        grouped[user].append(item)

    return render_template("high_risk.html", grouped_items=grouped)

@app.route("/spread-map")
def spread_map():
    if "username" not in session:
        return redirect("/login")
    return render_template("spread_map.html", graph=get_spread_map())

@app.route('/admin/users')
def view_users():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    users = get_all_users()  # Buat fungsi untuk ambil data user
    return render_template('admin_users.html', users=users)

@app.route('/admin/uploads')
def view_uploads():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    uploads = get_all_uploads()  # Buat fungsi ambil data upload
    return render_template('admin_uploads.html', uploads=uploads)

@app.route('/admin/flags')
def view_flags():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    flags = get_flagged_contents()  # Buat fungsi ambil data flagged
    return render_template('admin_flags.html', flags=flags)

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, role FROM users').fetchall()
    conn.close()
    return users

def get_all_uploads():
    conn = get_db_connection()
    uploads = conn.execute('SELECT * FROM uploads').fetchall()
    conn.close()
    return uploads

def get_flagged_contents():
    conn = get_db_connection()
    flags = conn.execute('''
        SELECT * FROM uploads
        WHERE flagged = 1
    ''').fetchall()
    conn.close()
    return flags

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    app.run(debug=True)
