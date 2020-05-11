from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SECRET_KEY'] = 'abc'
db = SQLAlchemy(app) 


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    session = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Id %r>' % self.id 

#route to do the operation
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        history = History.query.order_by(History.id).all()
        return render_template('index.html', history=history)

            
    numb1 = int(request.form.get("numb1"))
    ops = request.form.get("ops")
    numb2 = int(request.form.get("numb2"))

    if ops == "add":
        data = numb1 + numb2
        ops = "+"
    elif ops == "mul":
        data = numb1 * numb2
        ops = "*"
    elif ops == "div" and numb2 != 0:
        data = numb1 / numb2   
        ops = "/"    
    elif ops == "sub":
        data = numb1 - numb2
        ops = "-"
    else:
        data = "Invalid numbers"
        
    results = str(numb1) + " " + ops  + " " + str(numb2) + " = " + str(data)
    new_row = History(result=str(results))

    db.session.add(new_row)
    db.session.commit()

    flash(results)
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = History.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was problem in deleting the row"


#route to display tables
@app.route('/table', methods=['GET'])
def tables():
    num = request.values.get('table')
    return redirect(url_for('temp_table',num=num))

@app.route('/table/<int:num>')
def temp_table(num):
    return render_template('tables.html', n=num)

if __name__ == "__main__":
    app.run(debug=True)