from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

##Create Form
class NewCafe(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("URL Maps", validators=[DataRequired(), URL()])
    img_url = StringField("URL Image", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    has_toilet = SelectField("Has Toilet", choices=[("Yes"), ("No")])
    has_wifi = SelectField("Has Wifi", choices=[("Yes"), ("No")])
    has_sockets = SelectField("Has Sockets", choices=[("Yes"), ("No")])
    can_take_calls = SelectField("Can take Calls", choices=[("Yes"), ("No")])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit= SubmitField("Add/Edit Cafe")


@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=cafes)


## HTTP GET - Read Record
@app.route("/get/all")
def get_all():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/get/cafe/<int:index>")
def get_cafe(index):
    requested_cafe = Cafe.query.filter_by(id=index).first()
    return jsonify(cafe={
        "id": requested_cafe.id,
        "name": requested_cafe.name,
        "map_url": requested_cafe.map_url,
        "img_url": requested_cafe.img_url,
        "location": requested_cafe.location,
        "seats": requested_cafe.seats,
        "has_toilet": requested_cafe.has_toilet,
        "has_wifi": requested_cafe.has_wifi,
        "has_sockets": requested_cafe.has_sockets,
        "can_take_calls": requested_cafe.can_take_calls,
        "coffee_price": requested_cafe.coffee_price,
    })

@app.route("/cafe/<int:index>")
def show_cafe(index):
    requested_cafe = Cafe.query.filter_by(id=index).first()
    return render_template("cafe.html", cafe=requested_cafe)

## HTTP POST - Create Record
@app.route("/new", methods=["GET", "POST"])
def add_cafe():
    form = NewCafe()
    if form.validate_on_submit():
        cafe_name = form.name.data
        cafe_map_url = form.map_url.data
        cafe_img_url = form.img_url.data
        cafe_location = form.location.data
        cafe_seats = form.seats.data
        if form.has_toilet.data == "Yes":
            cafe_has_toilet = 1
        else:
            cafe_has_toilet = 0
        if form.has_wifi.data == "Yes":
            cafe_has_wifi = 1
        else:
            cafe_has_wifi = 0
        if form.has_sockets.data == "Yes":
            cafe_has_sockets = 1
        else:
            cafe_has_sockets = 0
        if form.can_take_calls.data == "Yes":
            cafe_can_take_calls = 1
        else:
            cafe_can_take_calls = 0
        cafe_coffee_price = form.coffee_price.data
        new_cafe = Cafe(name=cafe_name, map_url=cafe_map_url, img_url=cafe_img_url, location=cafe_location,
                        seats=cafe_seats, has_toilet=cafe_has_toilet, has_wifi=cafe_has_wifi,
                        has_sockets=cafe_has_sockets, can_take_calls=cafe_can_take_calls, coffee_price=cafe_coffee_price)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("new-cafe.html", form=form)

## HTTP PUT/PATCH - Update Record
@app.route("/update-cafe/<int:index>", methods=["GET", "POST"])
def update_cafe(index):
    cafe_id = index
    cafe_to_update = Cafe.query.get(index)
    form = NewCafe(name=cafe_to_update.name, map_url=cafe_to_update.map_url, img_url=cafe_to_update.img_url,
                   location=cafe_to_update.location, seats=cafe_to_update.seats, has_toilet=cafe_to_update.has_toilet,
                   has_wifi=cafe_to_update.has_wifi, has_sockets=cafe_to_update.has_sockets,
                   can_take_calls=cafe_to_update.can_take_calls, coffee_price=cafe_to_update.coffee_price)
    if form.validate_on_submit():
        cafe_to_update.name = form.name.data
        cafe_to_update.map_url = form.map_url.data
        cafe_to_update.img_url = form.img_url.data
        cafe_to_update.location = form.location.data
        cafe_to_update.seats = form.seats.data
        if form.has_toilet.data == "Yes":
            cafe_to_update.has_toilet = 1
        else:
            cafe_to_update.has_toilet = 0
        if form.has_wifi.data == "Yes":
            cafe_to_update.has_wifi = 1
        else:
            cafe_to_update.has_wifi = 0
        if form.has_sockets.data == "Yes":
            cafe_to_update.has_sockets = 1
        else:
            cafe_to_update.has_sockets = 0
        if form.can_take_calls.data == "Yes":
            cafe_to_update.can_take_calls = 1
        else:
            cafe_to_update.can_take_calls = 0
        cafe_to_update.coffee_price = form.coffee_price.data
        db.session.commit()
        return redirect(url_for('show_cafe', index=cafe_id))
    return render_template("new-cafe.html", cafe_id = cafe_id, form = form)
## HTTP DELETE - Delete Record
@app.route("/confirm-delete/<int:index>")
def confirm_delete(index):
    cafe_to_delete = Cafe.query.get(index)
    return render_template("confirm.html", cafe=cafe_to_delete)

@app.route("/delete-cafe/<int:index>")
def delete_cafe(index):
    cafe_to_delete = Cafe.query.get(index)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
