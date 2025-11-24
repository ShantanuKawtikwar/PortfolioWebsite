from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from models import db, Project, Certification, Timeline
import os

app = Flask(__name__)
app.secret_key = "super-secret"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

# File upload config
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Email Config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "YOUR_EMAIL@gmail.com"
app.config["MAIL_PASSWORD"] = "YOUR_APP_PASSWORD"
mail = Mail(app)


# ======================== PUBLIC ROUTES ========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=Project.query.all())

@app.route("/certifications")
def certifications():
    return render_template("certifications.html", certs=Certification.query.all())

@app.route("/timeline")
def timeline():
    return render_template("timeline.html", timeline=Timeline.query.all())

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        msg = Message(
            subject=f"Portfolio Message from: {request.form['name']}",
            sender=request.form["email"],
            recipients=[app.config["MAIL_USERNAME"]],
            body=f"Message:\n\n{request.form['message']}"
        )
        mail.send(msg)
        flash("Message sent ✔")
        return redirect("/contact")

    return render_template("contact.html")


# ======================== ADMIN ========================

@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin/dashboard")

        flash("Wrong username/password ❌")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session: return redirect("/admin")

    return render_template(
        "admin_dashboard.html",
        projects=Project.query.all(),
        certs=Certification.query.all(),
        timeline=Timeline.query.all()
    )


# ---------------- ADD / EDIT / DELETE UNIVERSAL ----------------

@app.route("/admin/add/<item>", methods=["GET","POST"])
def add_item(item):
    MODEL = {"project":Project,"cert":Certification,"timeline":Timeline}[item]

    if request.method == "POST":
        file = request.files.get("image")
        filename = secure_filename(file.filename) if file else None
        if file: file.save(os.path.join(UPLOAD_FOLDER, filename))

        data = MODEL(
            title=request.form.get("title"),
            description=request.form.get("desc"),
            issuer=request.form.get("issuer"),
            date=request.form.get("date"),
            month=request.form.get("month"),
            organization=request.form.get("org"),
            details=request.form.get("details"),
            image=filename
        )

        db.session.add(data)
        db.session.commit()
        return redirect("/admin/dashboard")

    return render_template("admin_form.html", mode=item, data=None)


@app.route("/admin/edit/<item>/<int:id>", methods=["GET","POST"])
def edit_item(item,id):
    MODEL = {"project":Project,"cert":Certification,"timeline":Timeline}[item]
    entry = MODEL.query.get(id)

    if request.method == "POST":
        if request.files.get("image"):
            filename = secure_filename(request.files["image"].filename)
            request.files["image"].save(os.path.join(UPLOAD_FOLDER, filename))
            entry.image = filename

        entry.title = request.form.get("title") or entry.title
        entry.description = request.form.get("desc") or entry.description
        entry.date = request.form.get("date") or entry.date
        entry.month = request.form.get("month") or entry.month
        entry.organization = request.form.get("org") or entry.organization
        entry.details = request.form.get("details") or entry.details
        entry.issuer = request.form.get("issuer") or entry.issuer

        db.session.commit()
        return redirect("/admin/dashboard")

    return render_template("admin_form.html", mode=item, data=entry)


@app.route("/admin/delete/<item>/<int:id>")
def delete_item(item,id):
    MODEL = {"project":Project,"cert":Certification,"timeline":Timeline}[item]
    db.session.delete(MODEL.query.get(id))
    db.session.commit()
    return redirect("/admin/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
