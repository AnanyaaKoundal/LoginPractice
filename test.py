from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
# app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Users.db"
db=SQLAlchemy(app)

class Members(db.Model):
    email=db.Column(db.String(50), nullable=False, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=False, primary_key=True)
    date_registered=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.email}"


@app.route('/', methods=['GET', 'POST'])
def helloworld():
    if request.method == 'POST':
        email=request.form['email']
        user=request.form['username']
        pas=request.form['password']
        e=Members(email=email, username=user, password=pas)
        db.session.add(e)
        db.session.commit()
    entry=Members.query.all()
    return render_template('index.html', entry=entry)
    
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        user=request.form['username']
        pas=request.form['password']
        e=Members(email=email, username=user, password=pas)
        db.session.add(e)
        db.session.commit()
        entry=Members.query.all()
        print('Abc')
        return render_template('index.html', entry=entry)
    return render_template('signup.html')

@app.route('/login.html')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)