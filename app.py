from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = process.env.URL
mongo = PyMongo(app)
db = mongo.db.infos

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        db.insert_one({"title":title,"desc":desc,"date_created":datetime.utcnow()})
        
    allTodo = db.find()
    length = db.count_documents({})
    return render_template('index.html', allTodo=allTodo,length=length)

@app.route('/update/<ObjectId:uid>', methods=['GET', 'POST'])
def update(uid):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        db.update_one({'_id':uid}, {"$set": {'title': title,'desc':desc}})
        return redirect("/")
        
    todo = db.find_one({"_id":uid})
    return render_template('update.html', todo=todo)

@app.route('/delete/<ObjectId:id>')
def delete(id):
    db.delete_one({"_id":id})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=process.env.PORT or 8000)
