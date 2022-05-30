from flask import Flask ,render_template , request ,redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///testing.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db =SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    current_date=db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) ->str:
        return f"{ self.sno }-{ self.title }"



@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':

        tit=request.form['title']
        des=request.form['descr']
        tst= Todo(title=tit, description=des)
        db.session.add(tst)
        db.session.commit()
    getTodo = Todo.query.all()

    return render_template('home.html', getTodo=getTodo)


@app.route("/delete/<int:sno>")
def delete(sno):

     getTodoForDelete = Todo.query.filter_by(sno=sno).first()
     db.session.delete(getTodoForDelete)
     db.session.commit()
     # print(getTodoForDelete)
     return redirect('/')

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        tit = request.form['title']
        des = request.form['descr']
        getTodoForUbdate = Todo.query.filter_by(sno=sno).first()
        getTodoForUbdate.title=tit
        getTodoForUbdate.description=des

        db.session.add(getTodoForUbdate)
        db.session.commit()
        return redirect('/')

    getTodoForUbdate = Todo.query.filter_by(sno=sno).first()

    return render_template('ubdate.html', getTodo=getTodoForUbdate)


@app.route("/about")
def About():
    return render_template('about.html')

# @app.route("/about")
# def About():
#     return "<h1>About</h1>"

if __name__ == "__main__":
    app.run(debug=True , port=8000)