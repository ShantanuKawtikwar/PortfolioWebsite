from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from models import db, Project, Certification, Timeline

app = Flask(__name__)
app.secret_key = "supersecret-key"

# DB Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


# ===== Email Config =====
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "contactshantanukawtikwar@gmail.com" 
app.config["MAIL_PASSWORD"] = "lfnu vstz ffrj jfcw"
mail = Mail(app)

# ========== Pages ==========
@app.route("/")
def home():
    projects = Project.query.all()
    certs = Certification.query.all()
    timeline = Timeline.query.all()
    return render_template("index.html", projects=projects, certs=certs, timeline=timeline)

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin/dashboard")
        flash("Invalid login", "danger")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin")
    return render_template("admin_dashboard.html")

@app.route("/admin/add/project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        project = Project(title=request.form["title"], description=request.form["desc"], date=request.form["date"])
        db.session.add(project)
        db.session.commit()
        return redirect("/admin/dashboard")
    return render_template("admin_forms.html", mode="project")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

