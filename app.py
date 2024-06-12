from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import Transform, sqlite3, joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
model = joblib.load("model.pkl")

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yogyakarta-housing-price.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    bed = db.Column(db.Integer, nullable=False)
    bath = db.Column(db.Integer, nullable=False)
    carport = db.Column(db.Integer, nullable=False)
    surface_area = db.Column(db.Integer, nullable=False)
    building_area = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


def add_property_to_db(locations, bed, bath, carport, surface_area, building_area, price):
    conn = sqlite3.connect('instance/yogyakarta-housing-price.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO properties (locations, bed, bath, carport, surface_area, building_area, price)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (locations, bed, bath, carport, surface_area, building_area, price))
    conn.commit()
    conn.close()

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    locations = [
    'Ngaglik, Sleman', 'Jombor, Sleman', 'Berbah, Sleman', 'Prambanan, Sleman', 'Moyudan, Sleman',
    'Depok, Sleman', 'Gamping, Sleman', 'Kaliurang, Yogyakarta', 'Sedayu, Bantul', 'Ngemplak, Sleman',
    'Piyungan, Bantul', 'Umbulharjo, Yogyakarta', 'Godean, Sleman', 'Mlati, Sleman', 'Condong Catur, Sleman',
    'Kasihan, Bantul', 'Bantul, Bantul', 'Sleman, Sleman', 'Sewon, Bantul', 'Kalasan, Sleman',
    'Plered, Bantul', 'Sleman, Yogyakarta', 'Maguwoharjo, Yogyakarta', 'Demangan, Yogyakarta',
    'Purwomartani, Sleman', 'Minggir, Sleman', 'Gondokusuman, Yogyakarta', 'Kotagede, Yogyakarta',
    'Turi, Sleman', 'Kaliurang, Sleman', 'Pogung, Yogyakarta', 'Mantrijeron, Yogyakarta', 'Cebongan, Sleman',
    'Pakualaman, Yogyakarta', 'Bantul, Yogyakarta', 'Sayegan, Sleman', 'Danurejan, Yogyakarta',
    'Wirobrajan, Yogyakarta', 'Banguntapan, Bantul', 'Seturan, Yogyakarta', 'Pakem, Sleman',
    'Caturtunggal, Sleman', 'Tegalrejo, Yogyakarta', 'Wonosari, Gunung Kidul', 'Jetis, Bantul',
    'Pajangan, Bantul', 'Kraton, Yogyakarta', 'Cebongan, Yogyakarta', 'Imogiri, Bantul', 'Sentolo, Kulon Progo',
    'Playen, Gunung Kidul', 'Tempel, Sleman', 'Kulonprogo, Kulon Progo', 'Mergangsan, Yogyakarta',
    'Wates, Kulon Progo', 'Gedong Tengen, Yogyakarta', 'Gondomanan, Yogyakarta', 'Jetis, Yogyakarta',
    'Sidoarum, Sleman', 'Nanggulan, Kulon Progo', 'Pandak, Bantul', 'Bambanglipuro, Bantul',
    'Imogiri, Yogyakarta', 'Nologaten, Yogyakarta', 'Caturtunggal, Yogyakarta', 'Kulonprogo, Yogyakarta',
    'Purwomartani, Yogyakarta', 'Sekip, Yogyakarta', 'Karangmojo, Gunung Kidul']

    price = None  # Inisialisasi predicted_price di luar blok if

    if request.method == 'POST':
        location = str(request.form['listing_location'])
        bed = int(request.form['bed'])
        bath = int(request.form['bath'])
        carport = int(request.form['carport'])
        surface_area = int(request.form['surface_area'])
        building_area = int(request.form['building_area'])


        data = [[location, bed, bath, carport, surface_area, building_area]]
        temp_df = pd.DataFrame(data, columns=['listing-location', 'bed', 'bath', 'carport', 'surface_area', 'building_area'])
        temp_df = pd.get_dummies(temp_df, columns=['listing-location'])
        temp_df = temp_df.reindex(columns=Transform.columns, fill_value=0)
        price = model.predict([temp_df.iloc[0]])

        new_property = Property(location=location, bed=bed, bath=bath, carport=carport, surface_area=surface_area,
                        building_area=building_area, price=price)

        db.session.add(new_property)
        db.session.commit()

    return render_template('index.html', locations=locations, price = price)


# Route to view all properties
@app.route('/properties')
def properties():
    all_properties = Property.query.all()
    return render_template('properties.html', properties=all_properties)
    

if __name__ == '__main__':
    app.run(debug=True)
