from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import requests
import json

app = Flask(__name__)
app.config["SECRET_KEY"] ="AtigyiUS9812892019IKOSNJSGDU"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

#db = SQLAlchemy()
#login_manager = LoginManager()
#login_manager.init_app(app)

#database
#class Users(UserMixin, db.Model):
   #id = db.Column(db.Integer, primary_key = True)



#db.init_app(app)
#with app.app_context:
   #db.create_all()

#@login_manager.user_loader
#def user_load(user_id):
   #return Users.query.get(user_id)

api_key = 'd2a23524be1e40038741925c6a3d3e0c'

#routes
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/recipe_names')
def recipe_names():
    if request.method == "POST":
        name = request.form.get("name")
        complex = "https://api.spoonacular.com/recipes/complexSearch"
        params ={'apiKey': api_key,
                 'query': name}
        response = requests.get(complex, params=params)
        val = json.loads(response.text)
        meal_ids = [val["results"][i]["id"] for i in range(len(val["results"]))]
        titles = [val["results"][i]["title"] for i in range(len(val["results"]))]
        images = [val["results"][i]["image"] for i in range(len(val["results"]))]
        





#main driver

if __name__ == "__main__":
    app.run(debug="True")
