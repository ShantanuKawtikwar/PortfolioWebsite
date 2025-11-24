from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "supersecret-key"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "contactshantanukawtikwar@gmail.com"
app.config["MAIL_PASSWORD"] = "lfnu vstz ffrj jfcw"

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/certifications")
def certifications():
    return render_template("certifications.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Mail content
        msg = Message(
            subject=f"Portfolio Contact From: {name}",
            sender=email,
            recipients=[app.config["MAIL_USERNAME"]]
        )
        msg.body = f"""
        You received a new message from your portfolio contact form:

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        try:
            mail.send(msg)
            flash("Message sent successfully! ✔️", "success")
        except Exception as e:
            print(e)
            flash("⚠️ Failed to send message. Try again later.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
