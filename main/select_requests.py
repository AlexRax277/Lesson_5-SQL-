from insert_requests import connection


def count_executors_in_genres():
    count_executors = connection.execute("""SELECT name_genre n, COUNT(genre_id) FROM genre_executor c
                                            JOIN genre ON c.genre_id = genre.id
                                            GROUP BY n
                                            ORDER BY -COUNT(genre_id)""").fetchall()
    return count_executors


def count_songs_in_albums():
    count_songs = connection.execute("""SELECT year_album, COUNT(year_album) FROM song
                                        JOIN album ON song.album_id = album.id
                                        GROUP BY year_album
                                        HAVING year_album BETWEEN 2019 and 2020""").fetchall()
    return count_songs


def avg_duration_songs_in_albums():
    avg_duration = connection.execute("""SELECT name_album, year_album, CAST(AVG(duration) as decimal(18,1)) FROM song
                                         JOIN album ON song.album_id = album.id
                                         GROUP BY name_album, year_album """).fetchall()
    return avg_duration


def executors_albums():
    executors = connection.execute("""SELECT name_executor FROM album
                                      JOIN executor_album ON executor_album.album_id = album.id 
                                      JOIN executor ON executor.id = executor_album.executor_id
                                      WHERE year_album NOT IN (2020)
                                      GROUP BY name_executor""").fetchall()
    return executors


def collections_include_executor(executor):
    collections = connection.execute(f"""SELECT name_collection FROM executor
                                                    JOIN executor_album ON executor.id = executor_album.executor_id
                                                    JOIN song ON executor_album.album_id = song.album_id 
                                                    JOIN song_collection ON song.id = song_collection.song_id
                                                    JOIN collection ON song_collection.collection_id = collection.id
                                                    WHERE name_executor = '{executor}'""").fetchall()
    return collections


def name_albums_genres():
    name_albums = connection.execute("""SELECT name_album, year_album, COUNT(genre_id) FROM genre_executor
                                        JOIN executor_album ON genre_executor.executor_id = executor_album.executor_id
                                        JOIN album ON executor_album.album_id = album.id
                                        GROUP BY name_album, year_album
                                        HAVING COUNT(genre_id) > 1""").fetchall()
    return name_albums


def name_songs_collections():
    name_songs = connection.execute("""SELECT name_song, COUNT(song_id) FROM song_collection
                                        JOIN song ON song_collection.song_id = song.id
                                        GROUP BY name_song
                                        HAVING COUNT(song_id) = 0""").fetchall()
    return name_songs


def name_executor_thr_shortest_song():
    name_executor = connection.execute("""SELECT name_executor, name_song, duration FROM song
                                        JOIN executor_album ON song.album_id = executor_album.album_id
                                        JOIN executor ON executor_album.executor_id = executor.id
                                        WHERE duration = (SELECT MIN(duration) FROM song)
                                        GROUP BY name_executor, name_song, duration""").fetchone()
    return name_executor


def name_albums_min_songs():
    name_albums = connection.execute("""SELECT MAX(name_album), year_album 
                                        FROM (SELECT name_album, year_album, COUNT(DISTINCT(album_id)) 
                                        FROM song as a JOIN album ON a.album_id = album.id
                                        GROUP BY name_album, year_album) as a
                                        GROUP BY name_album, year_album""").fetchall()
    return name_albums


if __name__ == '__main__':
    print(count_executors_in_genres())
    print(count_songs_in_albums())
    print(avg_duration_songs_in_albums())
    print(executors_albums())
    print(collections_include_executor('Bushido'))
    print(name_albums_genres())
    print(name_songs_collections())
    print(name_executor_thr_shortest_song())
    print(name_albums_min_songs())


