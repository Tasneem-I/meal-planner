from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] ="AtigyiUS9812892019IKOSNJSGDU"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

#database
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)



db.init_app(app)
with app.app_context:
    db.create_all()

@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(user_id)

#routes






#main driver

if __name__ == "__main__":
    app.run(debug="True")
