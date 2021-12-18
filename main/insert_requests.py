import csv
import sqlalchemy

db = 'postgresql://login:password@localhost:5432/firstproject'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

with open('data.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    songs_list = list(rows)


def data_insert(data):
    for string in data[1:]:
        genre = string[0]
        if connection.execute(f"""SELECT name_genre FROM genre WHERE name_genre = '{genre}'""").fetchone() is None:
            connection.execute(f"""INSERT INTO genre (name_genre) VALUES ('{genre}')""")

        executor = string[1]
        if connection.execute(
                f"""SELECT name_executor FROM executor WHERE name_executor = '{executor}'""").fetchone() is None:
            connection.execute(f"""INSERT INTO executor (name_executor) VALUES ('{executor}')""")

        try:
            connection.execute(f"""INSERT INTO genre_executor (genre_id, executor_id)
                               select(SELECT id FROM genre WHERE name_genre = '{genre}') as genre_id,
                               (SELECT id FROM executor WHERE name_executor = '{executor}') as executor_id""")
        except:
            pass

        album = string[4]
        year_album = string[5]
        if connection.execute(
                f"""SELECT name_album FROM album WHERE name_album = '{album}' 
                and year_album = '{year_album}'""").fetchone() is None:
            connection.execute(f"""INSERT INTO album (name_album, year_album) VALUES ('{album}', '{year_album}')""")

        try:
            connection.execute(f"""INSERT INTO executor_album (executor_id, album_id)
                               select(SELECT id FROM executor WHERE name_executor = '{executor}') as executor_id,
                               (SELECT id FROM album WHERE name_album = '{album}') as album_id""")
        except:
            pass

        song = string[2]
        duration = string[3]
        if connection.execute(f"""SELECT name_song FROM song WHERE name_song = '{song}'""").fetchone() is None:
            connection.execute(f"""INSERT INTO song (name_song, duration, album_id)
                                           VALUES ('{song}', '{duration}', 
                                           (SELECT id FROM album WHERE name_album = '{album}' 
                                           and year_album = '{year_album}'))""")

        collection = string[6]
        year_collection = string[7]
        if connection.execute(
                f"""SELECT name_collection FROM collection
                WHERE name_collection = '{collection}' and year_collection = '{year_collection}'""").fetchone() is None:
            connection.execute(
                f"""INSERT INTO collection (name_collection, year_collection)
                VALUES ('{collection}', '{year_collection}')""")

        try:
            connection.execute(f"""INSERT INTO song_collection (song_id, collection_id)
                               select(SELECT id FROM song WHERE name_song = '{song}') as song_id,
                               (SELECT id FROM collection WHERE name_collection = '{collection}') as collection_id""")
        except:
            pass


if __name__ == '__main__':
    data_insert(songs_list)
