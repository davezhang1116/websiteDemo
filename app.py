from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
#from flask_session import Session
import time
import os
from changelog import changelog
from login import login


file="data.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/{}'.format(file)
app.config['SECRET_KEY'] = 'password'
#app.config['SESSION_TYPE'] = 'sqlalchemy'
db = SQLAlchemy(app)
#app.config['SESSION_SQLALCHEMY'] = db
#sess = Session(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.String(100), default=time.strftime('%A %B, %d %Y %H:%M:%S'))
    #status = db.Column(db.Boolean, default=True)
    balance = db.Column(db.FLOAT, nullable = False)
    last_modified = db.Column(db.String(100), default=time.strftime('%A %B, %d %Y %H:%M:%S'))

    def __repr__(self):
        return '<Task %r>' % self.id




@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        wow = session['user']
    except:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['name']
        money = request.form['money']
        if name == "" or money == "":
            return redirect('/')
        else:
            new_task = Todo(name=name,balance=float(money))

            #try:
            db.session.add(new_task)
            db.session.commit()
            task = Todo.query.order_by(Todo.date_created.desc()).first()
            print(task.id, name,  0,  money,  "deposit",str(time.strftime('%A %B, %d %Y %H:%M:%S')))
            changelog(_ID=int(task.id)).create()
            changelog(_ID=int(task.id),_name= name, _initialBalance = 0, _finalBalance = money, _type = "deposit", _time = str(time.strftime('%A %B, %d %Y %H:%M:%S'))).store()

            return redirect('/')
            #except:
            #    return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/deposit/<int:id>', methods=['GET', 'POST'])
def deposit(id):
    try:
        wow = session['user']
    except:
        return render_template('login.html')

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':

        initial_balance = task.balance
        money = float(request.form['moneyDeposit'])
        task.balance = initial_balance + money
        task.last_modified = time.strftime('%A %B, %d %Y %H:%M:%S')
        #try:
        changelog(_ID=task.id,_name= task.name, _initialBalance = initial_balance, _finalBalance = task.balance, _type = "deposit", _time = str(time.strftime('%A %B, %d %Y %H:%M:%S').replace(",",""))).store()
        db.session.commit()

        return redirect('/')
        #except:
        #    return 'There was an issue updating your task'

    else:
        return render_template('deposit.html', task=task)

@app.route('/cost/<int:id>', methods=['GET', 'POST'])
def cost(id):
    try:
        wow = session['user']
    except:
        return render_template('login.html')

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':

        initial_balance = task.balance
        cost = float(request.form['moneyCost'])
        task.balance = initial_balance - cost
        task.last_modified = time.strftime('%A %B, %d %Y %H:%M:%S')

        #try:
        db.session.commit()
        changelog(_ID=task.id,_name= task.name, _initialBalance = initial_balance, _finalBalance = task.balance, _type = "cost", _time = str(time.strftime('%A %B, %d %Y %H:%M:%S').replace(",",""))).store()

        return redirect('/')
        #except:
        return 'There was an issue updating your task'

    else:
        return render_template('cost.html', task=task)

@app.route('/history/<int:id>', methods=['GET'])
def history(id):
    try:
        wow = session['user']
    except:
        return render_template('login.html')


    return changelog(id).read()

@app.route('/createaccount/', methods=['GET','POST'])
def createAccount():
    try:
        wow = session['user']
    except:
        return render_template('create.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "":
            return render_template('create.html')
        login(_username=username,_password=password).create()
        session["user"] = username
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/login/', methods=['GET','POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "":
            return render_template('login.html')
        if login(_username=username,_password=password).verify() == True:
            session["user"] = username
            return redirect('/')
        else:
            return 'Wrong username or password'
    else:
        return render_template('login.html')




if __name__ == "__main__":
    app.run(debug=True)
