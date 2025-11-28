import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Project, Certification, Timeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# CONFIGURATION
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"

# MAIL CONFIG (From .env)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)
db.init_app(app)

# Create upload folder if not exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# --- ADMIN CREDENTIALS (HASHED FOR SECURITY) ---
# Username: Shantanukawtikwar27
# Password: Prachi2711@$
ADMIN_USER = "Shantanukawtikwar27"
# This hash represents 'Prachi2711@$'
ADMIN_PASS_HASH = generate_password_hash("Prachi2711@$")

# --- CONTEXT PROCESSOR ---
# This injects the 'current_page' variable into all templates for active nav links
@app.context_processor
def inject_active():
    return dict(current_page=request.path)

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():
    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)

@app.route("/certifications")
def certifications():
    certs = Certification.query.all()
    return render_template("certifications.html", certs=certs)

@app.route("/timeline")
def timeline():
    timeline_data = Timeline.query.all()
    return render_template("timeline.html", timeline=timeline_data)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        try:
            msg = Message(
                subject=f"Portfolio Contact: {name}",
                sender=app.config["MAIL_USERNAME"],
                recipients=[app.config["MAIL_USERNAME"]],
                body=f"From: {name} <{email}>\n\n{message}"
            )
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {e}", "danger")
            
        return redirect(url_for("contact"))
    return render_template("contact.html")

# ================= ADMIN ROUTES =================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Credentials", "danger")
            
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    return render_template("admin_dashboard.html", 
                           projects=Project.query.all(), 
                           certs=Certification.query.all(), 
                           timeline=Timeline.query.all())

# --- GENERIC ADD/EDIT/DELETE ---

@app.route("/admin/add/<item_type>", methods=["GET", "POST"])
def add_item(item_type):
    if not session.get("admin_logged_in"): return redirect(url_for("admin_login"))

    MODELS = {"project": Project, "cert": Certification, "timeline": Timeline}
    ModelClass = MODELS.get(item_type)

    if request.method == "POST":
        file = request.files.get("image")
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # Dynamic data binding
        data = ModelClass()
        if item_type == "project":
            data.title = request.form.get("title")
            data.description = request.form.get("desc")
            data.tech_stack = request.form.get("tech")
            data.image = filename
        elif item_type == "cert":
            data.title = request.form.get("title")
            data.issuer = request.form.get("issuer")
            data.date = request.form.get("date")
            data.image = filename
        elif item_type == "timeline":
            data.year = request.form.get("year")
            data.title = request.form.get("title")
            data.organization = request.form.get("org")
            data.details = request.form.get("details")

        db.session.add(data)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("admin_form.html", mode="add", type=item_type)

@app.route("/admin/delete/<item_type>/<int:id>")
def delete_item(item_type, id):
    if not session.get("admin_logged_in"): return redirect(url_for("admin_login"))
    
    MODELS = {"project": Project, "cert": Certification, "timeline": Timeline}
    ModelClass = MODELS.get(item_type)
    
    item = ModelClass.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
