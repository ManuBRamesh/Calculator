from flask import Flask, render_template, request

app = Flask(__name__)

#main route
@app.route('/')
def index():
    return render_template('index.html')

#route to do the operation
@app.route('/operation', methods=['POST'])
def operation():
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
    return render_template('index.html', data=data, ops=ops, numb1=numb1,numb2=numb2)

if __name__ == "__main__":
    app.run(debug=True)