from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app) 


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Id %r>' % self.id 

#route to do the operation
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":           
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
        print("results   : "+ results)
        new_row = History(result=str(results))
    
        db.session.add(new_row)
        db.session.commit()
        history = History.query.order_by(History.id).all()
        return render_template('index.html', results=results, history=history)
  
    else:
        history = History.query.order_by(History.id).all()
        return render_template('index.html', history=history)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = History.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was problem in deducting the row"

if __name__ == "__main__":
    app.run(debug=True)