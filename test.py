from flask import Flask, render_template, request
from datetime import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Users.db"
app.config['SECRETKEY']="plantdiseaseproject"
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

class Members(db.Model):
    email=db.Column(db.String(50), nullable=False, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=False)
    date_registered=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.email}"

@app.route('/', methods=['GET', 'POST'])
def helloworld():
    entry=Members.query.all()
    return render_template('index.html', entry=entry)
    
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        user=request.form['username']
        pas=request.form['password']
        conn=sqlite3.connect('instance/users.db')
        con=conn.cursor()
        stat=f"SELECT * FROM members WHERE username='{user}' or email='{email}'"
        con.execute(stat)
        if con.fetchone():
            return render_template('signup.html', err=True)
        hashed_pas=bcrypt.generate_password_hash(pas)
        e=Members(email=email, username=user, password=hashed_pas)
        db.session.add(e)
        db.session.commit()
        entry=Members.query.all()
        print('Abc')
        return render_template('home.html', entry=entry)
    return render_template('signup.html')



@app.route('/login.html', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/loginval', methods=['GET', 'POST'])
def logcheck():
    ac=request.form['ans']
    pas=request.form['password']
    check=bcrypt.generate_password_hash(pas)
    conn=sqlite3.connect('instance/users.db')
    con=conn.cursor()
    err=False
    stat=f"SELECT * FROM members WHERE username='{ac}'"
    con.execute(stat)
    if con.fetchone():
        stat=f"SELECT password FROM members WHERE username='{ac}'"
        con.execute(stat)
        if bcrypt.check_password_hash(con.fetchone()[0], pas):
            return render_template('home.html')
    else:
        err=True
    return render_template('login.html', err=err)

@app.route('/home.html')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)