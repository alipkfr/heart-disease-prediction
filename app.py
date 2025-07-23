from flask import Flask, render_template, request, redirect, session, url_for, send_file, flash
from sqlite3 import *
from flask_mail import Mail, Message
from random import randrange
import pickle
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "monicaheart"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "alirussian99@gmail.com"
app.config["MAIL_PASSWORD"] = "ifgy vlax cqbi dmfh"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)

@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html", name=session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/find")
def find():
    if 'username' in session:
        return render_template("find.html", name=session['username'])
    else:
        return redirect(url_for('home'))

@app.route("/check", methods=["POST"])
def check():
    if request.method == "POST":
        if 'username' in session:
            name = session['username']
        age = float(request.form["age"])
        r1 = request.form["r1"]
        cp = int(r1) if r1 in ['1','2','3','4'] else 1
        BP = float(request.form["BP"])
        CH = float(request.form["CH"])
        maxhr = float(request.form["maxhr"])
        STD = float(request.form["STD"])
        fluro = float(request.form["fluro"])
        Th = float(request.form["Th"])
        d = [[age, cp, BP, CH, maxhr, STD, fluro, Th]]
        with open("models/heartdiseaseprediction.model", "rb") as f:
            model = pickle.load(f)
        res = model.predict(d)

        risk_percent = 80 if str(res[0]).strip().lower() == "presence" else 10

        session["report_data"] = {
            "age": age,
            "cp": cp,
            "BP": BP,
            "CH": CH,
            "maxhr": maxhr,
            "STD": STD,
            "fluro": fluro,
            "Th": Th,
            "result": 1 if res[0] == "Presence" else 0
        }

        try:
            con = connect("monicaheart.db")
            cursor = con.cursor()
            sql = """INSERT INTO predictions (username, age, cp, bp, ch, maxhr, std, fluro, th, result)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (name, age, cp, BP, CH, maxhr, STD, fluro, Th, str(res[0]).strip()))
            con.commit()
        except Exception as e:
            print("Error saving prediction:", e)
        finally:
            if con:
                con.close()

        return render_template("result.html", msg=str(res[0]).strip(), name=session['username'], risk_percent=risk_percent)
    else:
        return render_template("home.html")

@app.route("/download_pdf")
def download_pdf():
    if 'report_data' not in session:
        return redirect(url_for('home'))

    data = session["report_data"]
    filename = "heart_report.pdf"
    file_path = os.path.join("static", filename)
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Heart Disease Prediction Report")
    c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, f"Username: {session.get('username', 'Unknown')}")
    y = 680
    for key, val in data.items():
        c.drawString(100, y, f"{key}: {val}")
        y -= 20

    result_text = "Positive (At risk)" if data["result"] == 1 else "Negative (No signs of heart disease)"
    c.drawString(100, y - 10, f"Final Result: {result_text}")
    c.save()
    return send_file(file_path, as_attachment=True)

@app.route("/history")
def history():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        con = connect("monicaheart.db")
        cursor = con.cursor()
        cursor.execute("SELECT age, bp, ch, maxhr, result, timestamp FROM predictions WHERE username = ? ORDER BY timestamp DESC", (session['username'],))
        rows = cursor.fetchall()
        return render_template("history.html", name=session['username'], rows=rows)
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        if con:
            con.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        un = request.form.get("un")
        pw = request.form.get("pw")
        con = None
        try:
            con = connect("monicaheart.db")
            cursor = con.cursor()
            sql = "SELECT * FROM user WHERE username=? AND password=?"
            cursor.execute(sql, (un, pw))
            data = cursor.fetchall()
            if len(data) == 0:
                flash("Invalid login credentials", "danger")
                return redirect(url_for('login'))
            else:
                session['username'] = un
                flash(f"Welcome back, {un}!", "success")
                return redirect(url_for('home'))
        except Exception as e:
            flash("Issue: " + str(e), "danger")
            return redirect(url_for('login'))
        finally:
            if con:
                con.close()
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        em = request.form.get("em")
        un = request.form.get("un")
        pw = ""
        text = "0123456789"
        for i in range(6):
            pw += text[randrange(len(text))]

        if not firstname or not em or not un:
            flash("Please fill all required fields", "warning")
            return redirect(url_for('signup'))

        try:
            msg = Message("Welcome to HeartDiseasePrediction", sender="heartdiseasepredictorml@gmail.com", recipients=[em])
            msg.body = f"Greetings from HeartDiseasePredictor! Your password is {pw}"
            mail.send(msg)
        except Exception as e:
            flash("Failed to send email: " + str(e), "warning")
            return redirect(url_for('signup'))

        con = None
        try:
            con = connect("monicaheart.db")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM user WHERE username=?", (un,))
            if cursor.fetchone():
                flash("Username already exists!", "warning")
                return redirect(url_for('signup'))
            sql = "INSERT INTO user (username, password) VALUES (?, ?)"
            cursor.execute(sql, (un, pw))
            con.commit()
            flash("Account created successfully! Password sent to your email.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            if con:
                con.rollback()
            flash("Signup failed: " + str(e), "danger")
            return redirect(url_for('signup'))
        finally:
            if con:
                con.close()
    else:
        return render_template("signup.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        un = request.form.get("un")
        em = request.form.get("em")
        con = None
        try:
            con = connect('monicaheart.db')
            cursor = con.cursor()
            sql = "SELECT * FROM user WHERE username=?"
            cursor.execute(sql, (un,))
            data = cursor.fetchall()
            if len(data) == 0:
                flash("Invalid username!", "danger")
                return redirect(url_for('forgot'))
            else:
                pw1 = ""
                text = "0123456789"
                for i in range(6):
                    pw1 += text[randrange(len(text))]
                msg = Message("Hello again from HeartDiseasePrediction", sender="heartdiseasepredictorml@gmail.com", recipients=[em])
                msg.body = f"Greetings from HeartDiseasePredictor! Seems like you forgot your password. Your new password is {pw1}"
                mail.send(msg)
                try:
                    sql_update = "UPDATE user SET password=? WHERE username=?"
                    cursor.execute(sql_update, (pw1, un))
                    con.commit()
                    flash("Password has been mailed to you", "success")
                    return redirect(url_for('login'))
                except Exception as e:
                    con.rollback()
                    flash("Some Issue: " + str(e), "danger")
                    return redirect(url_for('forgot'))
        except Exception as e:
            flash("Issue " + str(e), "danger")
            return redirect(url_for('forgot'))
        finally:
            if con:
                con.close()
    else:
        return render_template("forgot.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/faq")
def faq():
    if 'username' in session:
        return render_template("faq.html", name=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
