CREATE TABLE IF NOT EXISTS genre (
	id SERIAL PRIMARY KEY,
	name_genre VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS executor (
	id SERIAL PRIMARY KEY,
	name_executor VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS genre_executor (
	genre_id INTEGER NOT NULL REFERENCES genre(id),
	executor_id INTEGER NOT NULL REFERENCES executor(id),
	CONSTRAINT ge PRIMARY KEY (genre_id, executor_id)
);

CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	name_album VARCHAR(40) NOT NULL,
	year_album INTEGER NOT NULL CHECK(year_album > 0)
);

CREATE TABLE IF NOT EXISTS executor_album (
	executor_id INTEGER NOT NULL REFERENCES executor(id),
	album_id INTEGER NOT NULL REFERENCES album(id),
	CONSTRAINT ea PRIMARY KEY (executor_id, album_id)
);

CREATE TABLE IF NOT EXISTS song (
	id SERIAL PRIMARY KEY,
	name_song VARCHAR(40) NOT NULL UNIQUE,
	duration INTEGER NOT NULL CHECK(duration > 0),
	album_id INTEGER NOT NULL REFERENCES album(id)
);

CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	name_collection VARCHAR(40) NOT NULL UNIQUE,
	year_collection INTEGER NOT NULL CHECK(year_collection > 0)
);

CREATE TABLE IF NOT EXISTS song_collection (
	song_id INTEGER NOT NULL REFERENCES song(id),
	collection_id INTEGER NOT NULL REFERENCES collection(id),
	CONSTRAINT sc PRIMARY KEY (song_id, collection_id)
);


