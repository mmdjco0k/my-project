from flask import Flask , redirect , render_template , request , session , url_for
import mysql.connector
import hashlib
from email.message import EmailMessage
import ssl
import smtplib
import random

app = Flask(__name__)
app.secret_key="2077"

mydb = mysql.connector.connect(
host = "127.0.0.1",
user = "root",
password = "2077",
database = "login_page"
)

cursor = mydb.cursor()
print(mydb)

def reset_password(email_recever):
    def generate_password():
        length = 8
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+"
        password = ""
        for i in range(length):
            password += random.choice(characters)
        print("Your generated password is:", password)
        return password

    new_passw = generate_password()


    email_sender = "mohamadrezamehrabimoghadam@gmail.com"
    passw = "mbvf aizn wwfd djyp"
    subject = "your new password"
    body = f"""your new password is 
    `{new_passw}`"""

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_recever
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp :
        smtp.login(email_sender,passw)
        smtp.sendmail(email_sender,email_recever,em.as_string())
    return new_passw

@app.route("/")
def main():
    ip_addr = request.remote_addr
    return render_template("pages/main.html",ip = ip_addr )


@app.route("/lo")
def lo():
    return render_template("pages/signup.html")

@app.route("/signup/" , methods = ["POST"])
def signup():
    
    u = hashlib.sha256()
    p = hashlib.sha256()
    
    cursor = mydb.cursor()
    if request.method == "POST":
        user = request.form['username']
        password = request.form['PW']
        gmail = request.form["gmail"]
        u.update(user.encode())
        p.update(password.encode())

        if password != "" and len(password)>=8:
            usr = u.hexdigest()
            pw = p.hexdigest()
            
            sqlFurmola = "INSERT INTO user_pass ( users , Pass , Email) VALUES (%s , %s , %s)"
            sqlFurmola1 = (usr,pw,gmail)
            cursor.execute(sqlFurmola , sqlFurmola1)
            mydb.commit()
            return  redirect(url_for('main'))
        else :
            return render_template("pages/signup-alert.html")

@app.route("/ll")
def ll():
    return render_template("pages/login.html")

@app.route("/loginn",methods = ["POST"])
def login():
    u = hashlib.sha256()
    p = hashlib.sha256()
    
    cursor = mydb.cursor()
    if request.method == "POST":
        username = request.form["username"]
        paasword = request.form["PW"]
        
    u.update(username.encode())
    p.update(paasword.encode())
    
    usr = u.hexdigest()
    pw = p.hexdigest()
    
    cursor.execute(f"SELECT * FROM user_pass where users = %s and Pass = %s ",(usr,pw))
    result = cursor.fetchall() 
    l = len(result)   
    print(l)
    if l == 1:
        for i in result:
            if i[1] == pw:
                ip_addr = request.remote_addr
                session['username'] = username.encode()
                return render_template("pages/main_2.html" , ip = ip_addr)

            else :
                return render_template("pages/alert.html")
    else:
        return render_template("pages/alert.html")

@app.route("/frg-psw")
def forget_psw():
    return render_template("pages/forget.html")

@app.route("/forget",methods = ["POST"])
def forget_password():    
    if request.method == "POST":
        username = request.form["usr"]
        email = request.form["gmail"]
    u = hashlib.sha256()
    p = hashlib.sha256()
    u.update(username.encode())
    usr = u.hexdigest()
    
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM user_pass where users = %s and Email = %s ;",(usr,email))
    result = cursor.fetchall()
    print(result)
    l = len(result)
    if l ==  1:
        for i in result :
            if i[2] == email:
                new_password = reset_password(email)
                p.update(new_password.encode())
                pw = p.hexdigest()
                cursor2 = mydb.cursor()
                
                sqlFurmola = "UPDATE user_pass SET Pass = %s WHERE Email = %s AND users = %s;"
                sqlFurmola1 = (pw,email ,usr)
                cursor2.execute(sqlFurmola,sqlFurmola1)
                mydb.commit()
                return render_template("pages/login.html")
    else : 
        return render_template("pages/forget-alert.html")

    

@app.route("/logout")
def logout():
    session.pop('username', default=None)
    return redirect(url_for("main"))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=81)