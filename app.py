from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Define the Location model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    properties = db.relationship('Property', backref='location', lazy=True)


# Define the Property model
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    bed = db.Column(db.Integer, nullable=False)
    bath = db.Column(db.Integer, nullable=False)
    carport = db.Column(db.Integer, nullable=False)
    surface_area = db.Column(db.Integer, nullable=False)
    building_area = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    locations = Location.query.all()  # Retrieve all locations from the database
    price = None
    if request.method == 'POST':
        location_id = int(request.form['listing_location'])
        bed = int(request.form['bed'])
        bath = int(request.form['bath'])
        carport = int(request.form['carport'])
        surface_area = int(request.form['surface_area'])
        building_area = int(request.form['building_area'])

        # Sample price calculation (replace with your own logic)
        price = (bed * 1000) + (bath * 500) + (carport * 300) + (surface_area * 50) + (building_area * 100)

        # Create a new Property instance and save it to the database
        new_property = Property(location_id=location_id, bed=bed, bath=bath, carport=carport, surface_area=surface_area,
                                building_area=building_area, price=price)
        db.session.add(new_property)
        db.session.commit()

    return render_template('index.html', locations=locations, price=price)


# Route to view all properties
@app.route('/properties')
def properties():
    all_properties = Property.query.all()
    return render_template('properties.html', properties=all_properties)


if __name__ == '__main__':
    app.run(debug=True)
