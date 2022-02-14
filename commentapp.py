from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 
 
app = Flask(__name__)
 

app.secret_key = 'Yashamma'
 
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '@Sureshvijaya12'
app.config['MYSQL_DATABASE_DB'] = 'sravandb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/Signin/', methods=['GET', 'POST'])
def signin():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM commentapp WHERE email = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['secret'] = account['secret']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    
    return render_template('Signin.html')
 
@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'secretcode' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        secretcode = request.form['secretcode']
        fullname = request.form['fullname']

        cursor.execute('SELECT * FROM commentapp WHERE email = %s', (email))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is invalid, now insert new account into commentapp table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form!'
    return render_template('Signup.html', msg=msg)

def forgot():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST' and 'email' in request.form and 'secretcode' in request.form:
        email = request.form['email']
        secretcode = request.form['secretcode']
        cursor.execute('SELECT * FROM commentapp WHERE email = %s AND secretcode = %d', (username, secretcode))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['secretcode'] = account['secretcode']
            return render_template('forgotpassword.html'))
    
    return render_template('Signin.html')
   

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the welcome page
        return render_template('welcomepage.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('signin'))

@app.route('/Signout')
def logout():
    # Remove session data, this will log the user out
   if account:
      return render_template('Thankyou.html')
   # Redirect to login page
   return redirect(url_for('signin'))

@app.route('/welcome')
def welcome(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM commentapp WHERE email = %s AND fullname =%s', email=session['email'],fullname=session['fullname])
        account = cursor.fetchone()
        return render_template('welcomepage.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
  
  
if __name__ == '__main__':
    app.run(debug=True)