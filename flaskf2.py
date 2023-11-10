from flask import Flask , redirect , render_template , request , session , url_for
import mysql.connector
import hashlib

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
        u.update(user.encode())
        p.update(password.encode())
        if password != "" and len(password)>=8:
            usr = u.hexdigest()
            pw = p.hexdigest()
            
            sqlFurmola = "INSERT INTO user_pass ( users , Pass) VALUES (%s , %s)"
            sqlFurmola1 = (usr,pw)
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


@app.route("/logout")
def logout():
    session.pop('username', default=None)
    return redirect(url_for("main"))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=81)