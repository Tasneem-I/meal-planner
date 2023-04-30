from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_session import Session
import requests
import json

app = Flask(__name__)
app.config["SECRET_KEY"] ="AtigyiUS9812892019IKOSNJSGDU"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

#database
class Users(UserMixin, db.Model):
   id = db.Column(db.Integer, primary_key = True)
   firstname = db.Column(db.String(40), nullable = False)
   lastname = db.Column(db.String(40), nullable=False)
   email = db.Column(db.String(50), unique = True, nullable = False)
   password = db.Column(db.String, nullable= False)
   username = db.Column(db.String(40), nullable = False)
   hash = db.Column(db.String(40), nullable = False)
   sppassword = db.Column(db.String, nullable= False)





db.init_app(app)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_load(user_id):
   return Users.query.get(user_id)

api_key = 'd2a23524be1e40038741925c6a3d3e0c'

#routes
@app.route('/')
def fact_json():
    url = "https://api.spoonacular.com/food/trivia/random"
    params = {"apiKey": api_key}
    response = requests.get(url, params=params)
    fact = json.loads(response.text)["text"]
    return render_template("home.html", fact=fact)





@app.route('/recipe_names', methods=["GET", "POST"])
def recipe_names():
    if request.method == "POST":
        name = request.form.get("name")
        complex = "https://api.spoonacular.com/recipes/complexSearch"
        params ={'apiKey': api_key,
                 'query': name,
                 'number' : 4} #REQUIRES CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        response = requests.get(complex, params=params)
        val = json.loads(response.text)
        meal_ids = [val["results"][i]["id"] for i in range(len(val["results"]))]
        titles = [val["results"][i]["title"] for i in range(len(val["results"]))]
        recipe_cards = []
        for i in meal_ids:
            place = "https://api.spoonacular.com/recipes/"+str(i)+"/card"
            param = {'apiKey' : api_key}
            results = requests.get(place, params=param)
            final = json.loads(results.text)
            card = final["url"]
            recipe_cards.append(card)
        
        return render_template("recipes_by_name.html",cards = recipe_cards, titles=titles)
    else:
        return render_template("recipes_by_name.html")
    

@app.route('/recipe_search', methods=["GET", "POST"])
def recipe_search():
    if request.method == "POST":
        Incingredients = request.form.get("ingredients_inc")
        Excingredients = request.form.get("ingredients_exc")
        diet = request.form.get("diet")
        complex = "https://api.spoonacular.com/recipes/complexSearch"
        params ={'apiKey': api_key,
                 'diet': diet,
                 'includeIngredients' : Incingredients,
                 'excludeIngredients' : Excingredients,
                 'number' : 4} #REQUIRES CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        response = requests.get(complex, params=params)
        val = json.loads(response.text)
        meal_ids = [val["results"][i]["id"] for i in range(len(val["results"]))]
        titles = [val["results"][i]["title"] for i in range(len(val["results"]))]
        recipe_cards = []
        for i in meal_ids:
            place = "https://api.spoonacular.com/recipes/"+str(i)+"/card"
            param = {'apiKey' : api_key}
            results = requests.get(place, params=param)
            final = json.loads(results.text)
            card = final["url"]
            recipe_cards.append(card)
        
        return render_template("recipes_search.html",cards= recipe_cards, titles=titles)
    else:
        return render_template("recipes_search.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        call = "https://api.spoonacular.com/users/connect?apiKey=" + api_key
        post = json.dumps({
            'firstName' : firstname,
            'lastName' : lastname,
            'email' : email
        })
        header = {'Content-Type':'application/json'}
        response = requests.request(method="POST",url=call,headers = header, data=post)
        result = json.loads(response.text)
        username = result["username"]
        hash = result["hash"]
        sppassword = result["spoonacularPassword"]
        user = Users(firstname=firstname, lastname=lastname, email=email, password=password, username=username, hash=hash,sppassword=sppassword)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    else:   
        return render_template("signup.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(email = request.form.get("email")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            session["user"] = user
            return redirect(url_for("mealplan"))
    return render_template("login.html")


@app.route("/mealplan", methods=["GET", "POST"])
def mealplan():
    if request.method == "POST":
        gen = 'https://api.spoonacular.com/mealplanner/generate'
        key = 'd2a23524be1e40038741925c6a3d3e0c'
        user = session.get('user')
        diet = request.form.get("diet")
        exc = request.form.get("excIng")
        cal = request.form.get("calories")
        params ={"apiKey": key, "timeFrame": 'week', 'diet' : diet, "exclude": exc, "targetCalories": cal}
        ans = requests.get(gen, params=params)
        plan = json.loads(ans.text)
        meal_ids =[]
        meal_servings =[]
        meal_prep =[]
        meal_names = []
        source = []
        for days in mealplan["week"]:
            for i in range(0,3):
                id =mealplan["week"][days]["meals"][i]["id"]
                food =mealplan["week"][days]["meals"][i]["title"]
                link =mealplan["week"][days]["meals"][i]["sourceUrl"]
                meal_ids.append(id)
                meal_names.append(food)
                source.append(link)
        cards=[]
        for id in meal_ids:
            url = "https://api.spoonacular.com/recipes/" + str(id)+ "/card"
            get_1 = requests.get(url)
            get = json.loads(get_1)
            image = get["image"]
            cards.append(image)
        
        return render_template("mealplan.html", meals = meal_names,images= cards, links = source)
    else:
        return render_template("mealplan.html")


        
        




#main driver

if __name__ == "__main__":
    app.run(debug="True")
