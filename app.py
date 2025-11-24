from flask import Flask, render_template, json

app = Flask(__name__)

# Helper function to load JSON files
def load_data(filename):
    with open(f"data/{filename}.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/projects")
def projects():
    projects = load_data("projects")
    return render_template("projects.html", title="Projects", projects=projects)


@app.route("/certifications")
def certifications():
    certs = load_data("certifications")
    return render_template("certifications.html", title="Certifications", certs=certs)


@app.route("/timeline")
def timeline():
    timeline_events = load_data("timeline")
    return render_template("timeline.html", title="Timeline", timeline=timeline_events)


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
