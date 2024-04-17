from api.database import db

genres = ['first', 'second', '...']

for genre in genres:
    db.add_genre(genre=genre)
