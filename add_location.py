from app import app, db, Location

# List of locations to add
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
    'Purwomartani, Yogyakarta', 'Sekip, Yogyakarta', 'Karangmojo, Gunung Kidul'
]

with app.app_context():
    db.create_all()  # Ensure the database tables are created
    for loc in locations:
        if not Location.query.filter_by(name=loc).first():
            db.session.add(Location(name=loc))
    db.session.commit()
