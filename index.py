# an object of WSGI application
from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import subprocess
# Flask constructor
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_DB"] = "py_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# A decorator used to tell the application
# which URL is associated function


@app.route('/', methods=['GET', 'POST'])
def home():
   if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sys_username = request.form['sys_username']
        sys_ip = request.form['sys_ip']
        sys_password = request.form['sys_password']

        
        con = mysql.connection.cursor()
        sql = "INSERT INTO users (name, email, sys_username, sys_ip, sys_password) VALUES (%s, %s, %s, %s, %s)"
        val = (name, email, sys_username, sys_ip, sys_password)
        con.execute(sql, val)
        mysql.connection.commit()      
        return redirect(url_for('sucesspage'))  # Redirect to sucess page after adding user
    
   return(render_template("homepage.html"))

 
@app.route('/sucess')
def sucesspage():
    return render_template("sucess.html")

@app.route('/py_run', methods=['GET', 'POST'])
def run_code():
    run_result = subprocess.run(['python', 'shop_install.py'], capture_output=True, text=True)
    return run_result.stdout


if __name__=='__main__':
   app.run(debug=True)