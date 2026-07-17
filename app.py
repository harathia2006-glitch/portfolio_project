from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Secret key
app.secret_key = "portfolio_secret"


# Upload folder configuration
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create upload folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# ---------------- DATABASE ----------------

def get_db():

    conn = sqlite3.connect("portfolio.db")

    conn.row_factory = sqlite3.Row

    return conn



def create_tables():

    conn = get_db()

    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS about(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        father TEXT,
        mother TEXT,
        dob TEXT,
        gender TEXT,
        address TEXT,
        email TEXT,
        phone TEXT,
        objective TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS education(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college TEXT,
        university TEXT,
        branch TEXT,
        degree TEXT,
        year TEXT,
        cgpa TEXT,
        intercollege TEXT,
        intermarks TEXT,
        school TEXT,
        sscmarks TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        programming TEXT,
        technical TEXT,
        softskills TEXT,
        languages TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS activities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workshop TEXT,
        seminar TEXT,
        internship TEXT,
        hackathon TEXT,
        sports TEXT,
        volunteer TEXT,
        extracurricular TEXT,
        activity_date TEXT,
        description TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS achievements(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        category TEXT,
        date TEXT,
        organization TEXT,
        description TEXT,
        certificate TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        category TEXT,
        technology TEXT,
        duration TEXT,
        github TEXT,
        description TEXT,
        status TEXT,
        image TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS certificates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certificate_name TEXT,
        certificate_type TEXT,
        organization TEXT,
        issue_date TEXT,
        description TEXT,
        file TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        photo TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS contact(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        email TEXT,
        linkedin TEXT,
        github TEXT,
        website TEXT,
        address TEXT,
        message TEXT
    )
    """)



    conn.commit()

    conn.close()



# ---------------- HOME ----------------


@app.route("/")
def home():

    return render_template("index.html")



# ---------------- ABOUT ----------------


@app.route("/about")
def about():

    return render_template("about.html")



@app.route("/save_about", methods=["POST"])
def save_about():

    conn=get_db()

    conn.execute("""
    INSERT INTO about
    VALUES(NULL,?,?,?,?,?,?,?,?,?)
    """,
    (
    request.form["fullname"],
    request.form["father"],
    request.form["mother"],
    request.form["dob"],
    request.form["gender"],
    request.form["address"],
    request.form["email"],
    request.form["phone"],
    request.form["objective"]
    ))

    conn.commit()

    conn.close()

    return "About Details Saved Successfully"



# ---------------- EDUCATION ----------------


@app.route("/education")
def education():

    return render_template("education.html")



@app.route("/save_education",methods=["POST"])
def save_education():

    conn=get_db()

    conn.execute("""
    INSERT INTO education VALUES(NULL,?,?,?,?,?,?,?,?,?,?)
    """,
    (
    request.form["college"],
    request.form["university"],
    request.form["branch"],
    request.form["degree"],
    request.form["year"],
    request.form["cgpa"],
    request.form["intercollege"],
    request.form["intermarks"],
    request.form["school"],
    request.form["sscmarks"]
    ))

    conn.commit()

    conn.close()

    return "Education Saved Successfully"



# ---------------- SKILLS ----------------


@app.route("/skills")
def skills():

    return render_template("skills.html")



@app.route("/save_skills",methods=["POST"])
def save_skills():

    conn=get_db()

    programming=",".join(request.form.getlist("skills"))

    conn.execute("""
    INSERT INTO skills VALUES(NULL,?,?,?,?)
    """,
    (
    programming,
    request.form["technical"],
    request.form["softskills"],
    request.form["languages"]
    ))

    conn.commit()

    conn.close()

    return "Skills Saved Successfully"



# ---------------- ACTIVITIES ----------------


@app.route("/activities")
def activities():

    return render_template("activities.html")



@app.route("/save_activities",methods=["POST"])
def save_activities():

    conn=get_db()

    conn.execute("""
    INSERT INTO activities VALUES(NULL,?,?,?,?,?,?,?,?,?)
    """,
    (
    request.form["workshop"],
    request.form["seminar"],
    request.form["internship"],
    request.form["hackathon"],
    request.form["sports"],
    request.form["volunteer"],
    request.form["extracurricular"],
    request.form["activity_date"],
    request.form["description"]
    ))

    conn.commit()

    conn.close()

    return "Activities Saved Successfully"



# ---------------- ACHIEVEMENTS ----------------


@app.route("/achievements")
def achievements():

    return render_template("achievements.html")



@app.route("/save_achievements",methods=["POST"])
def save_achievements():

    file=request.files["certificate"]

    filename=""

    if file.filename:
        filename=secure_filename(file.filename)
        file.save(
        os.path.join(
        UPLOAD_FOLDER,
        filename))


    conn=get_db()

    conn.execute("""
    INSERT INTO achievements VALUES(NULL,?,?,?,?,?,?)
    """,
    (
    request.form["title"],
    request.form["category"],
    request.form["date"],
    request.form["organization"],
    request.form["description"],
    filename
    ))

    conn.commit()

    conn.close()


    return "Achievement Saved Successfully"



# ---------------- PROJECTS ----------------


@app.route("/projects")
def projects():

    return render_template("projects.html")



@app.route("/save_projects",methods=["POST"])
def save_projects():

    image=request.files["project_image"]

    filename=""

    if image.filename:

        filename=secure_filename(image.filename)

        image.save(
        os.path.join(
        UPLOAD_FOLDER,
        filename))


    conn=get_db()

    conn.execute("""
    INSERT INTO projects VALUES(NULL,?,?,?,?,?,?,?,?)
    """,
    (
    request.form["project_name"],
    request.form["category"],
    request.form["technology"],
    request.form["duration"],
    request.form["github"],
    request.form["description"],
    request.form["status"],
    filename
    ))


    conn.commit()

    conn.close()

    return "Project Saved Successfully"



# ---------------- CERTIFICATES ----------------


@app.route("/certificates")
def certificates():

    return render_template("certificates.html")



@app.route("/save_certificates",methods=["POST"])
def save_certificates():

    file=request.files["certificate_file"]

    filename=""

    if file.filename:

        filename=secure_filename(file.filename)

        file.save(
        os.path.join(
        UPLOAD_FOLDER,
        filename))


    conn=get_db()

    conn.execute("""
    INSERT INTO certificates VALUES(NULL,?,?,?,?,?,?)
    """,
    (
    request.form["certificate_name"],
    request.form["certificate_type"],
    request.form["organization"],
    request.form["issue_date"],
    request.form["description"],
    filename
    ))


    conn.commit()

    conn.close()


    return "Certificate Saved Successfully"



# ---------------- PROFILE ----------------


@app.route("/profile")
def profile():

    return render_template("profile.html")



@app.route("/upload_profile",methods=["POST"])
def upload_profile():

    photo=request.files["profile_photo"]

    filename=secure_filename(photo.filename)

    photo.save(
    os.path.join(
    UPLOAD_FOLDER,
    filename))


    conn=get_db()

    conn.execute(
    "INSERT INTO profile VALUES(NULL,?)",
    (filename,)
    )

    conn.commit()

    conn.close()


    return "Profile Photo Uploaded Successfully"



# ---------------- CONTACT ----------------


@app.route("/contact")
def contact():

    return render_template("contact.html")



@app.route("/save_contact",methods=["POST"])
def save_contact():

    conn=get_db()

    conn.execute("""
    INSERT INTO contact VALUES(NULL,?,?,?,?,?,?,?)
    """,
    (
    request.form["phone"],
    request.form["email"],
    request.form["linkedin"],
    request.form["github"],
    request.form["website"],
    request.form["address"],
    request.form["message"]
    ))


    conn.commit()

    conn.close()


    return "Contact Details Saved Successfully"



# Run Application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

