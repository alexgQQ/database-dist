from abc import ABC, abstractmethod
from datetime import date
from math import log
from random import choice, choices, randint, sample, uniform
from typing import Any

from database import Album, Artist, ArtistTrackJoin, Genre, Label, SubGenre, Track
from genres import genre_list
from names import (
    AlbumNameGenerator,
    ArtistNameGenerator,
    LabelNameGenerator,
    SongNameGenerator,
    fake,
)

artist_names = ArtistNameGenerator()
album_names = AlbumNameGenerator()
track_names = SongNameGenerator()
label_names = LabelNameGenerator()


# I wanted to be able to generate a random set of numbers whose sum would be guaranteed
# but I wasn't sure if it was a solvable problem. Ended up finding the [Dirichlet distribution](https://en.wikipedia.org/wiki/Dirichlet_distribution)
# but there wasn't a very simple implementation. Ended up following [this](https://stackoverflow.com/a/29187687)
# to do a simpler exponential distribution for an approximation, it's ~6% off of target size usually
# Additionally I wanted to try to make this real efficient and do it in a functional sort of way.
# Hence the usage of maps/generators, it is remarkably faster.
def distribute(target: int, size: int) -> Any:
    def normalize(iter):
        iter = tuple(iter)
        iter_sum = sum(iter)

        for value in iter:
            yield value / iter_sum

    def scale(offset):
        low_boundary = 1
        upper_boundary = target - 1
        return int(low_boundary + (offset * upper_boundary))

    samples = map(lambda x: uniform(0.0, 1.0), range(size))
    values = map(lambda x: -1 * log(x), samples)
    offsets = normalize(values)
    return map(scale, offsets)


class IDObjectGenerator(ABC):
    """
    Abstract class structure for creating and storing data with incrementing ids.
    Helpful for managing data with ids between relationships in a SQL structure.
    Each call will generate the defined data, append an id as a key
    and save the entry to the `data` attr
    """

    # sqlalchemy equivalent for mapping
    schema_class = None

    def __init__(self, offset=0) -> None:
        self.first_id = offset + 1
        self.next_id = self.first_id
        self.data = []

    def __call__(self, *args, **kwargs) -> dict:
        data = self.get_data(*args, **kwargs)
        data.update({"id": self.next_id})
        self.data.append(data)
        self.next_id += 1
        return data

    @abstractmethod
    def get_data(self) -> dict:
        """Implement this for data factories with id generation"""
        return {}


class LabelGenerator(IDObjectGenerator):

    schema_class = Label

    def get_data(self) -> dict:
        return {
            "name": label_names(),
        }


class AlbumGenerator(IDObjectGenerator):

    schema_class = Album

    def get_data(self, label_id: int) -> dict:
        return {
            "name": album_names(),
            "label_id": label_id,
            "release_date": fake.date_between(date(1990, 1, 1), date.today()),
        }


class TrackGenerator(IDObjectGenerator):

    schema_class = Track

    def get_data(self, album_id: int, genre_id: int, subgenre_id: int) -> dict:
        return {
            "album_id": album_id,
            "name": track_names(),
            "genre_id": genre_id,
            "sub_genre_id": subgenre_id,
            "length": uniform(1.0, 6.0),
        }


class ArtistGenerator(IDObjectGenerator):

    schema_class = Artist

    def get_data(self) -> dict:
        return {
            "name": artist_names(),
        }


class ArtistTrackJoinGenerator(IDObjectGenerator):

    schema_class = ArtistTrackJoin

    def get_data(self, artist_id: int, track_id: int) -> dict:
        return {
            "artist_id": artist_id,
            "track_id": track_id,
        }


class GenreGenerator(IDObjectGenerator):

    schema_class = Genre

    def get_data(self, name: str) -> dict:
        return {
            "name": name,
        }


class SubGenreGenerator(IDObjectGenerator):

    schema_class = SubGenre

    def get_data(self, name: str, genre_id: int) -> dict:
        return {
            "name": name,
            "genre_id": genre_id,
        }


class BulkFactory:
    """
    Factory functionality for creating album data in bulk.
    This works by managing the data and ids for our models
    outside of sqlalchemy and bulk inserting them with their
    related mapping. Basically performs large `INSERT INTO`
    statements without the need to fetch related ids.
    """

    def __init__(self, session_pool: Any) -> None:
        self.session = session_pool

        # Might be a better pattern for all this but this works for now
        self.labels = LabelGenerator()
        self.albums = AlbumGenerator()
        self.tracks = TrackGenerator()
        self.artists = ArtistGenerator()
        self.artist_joins = ArtistTrackJoinGenerator()
        self.genres = GenreGenerator()
        self.subgenres = SubGenreGenerator()

        # Order matters here since writes happen in this order, labels must be written before their albums
        self.generators = [
            self.labels,
            self.albums,
            self.tracks,
            self.artists,
            self.artist_joins,
            self.genres,
            self.subgenres,
        ]

    def create_genres(self):
        """Create genre and subgenre entries from a hardcoded list"""
        # We'll need these genre ids for creating tracks later
        self.genre_ids = {}
        for genre in genre_list:
            subgenres = genre["subgenres"]
            genre = self.genres(genre["genre"])
            genre_id = genre["id"]

            subgenre_ids = []
            for subgenre_name in subgenres:
                subgenre = self.subgenres(subgenre_name, genre_id)
                subgenre_ids.append(subgenre["id"])

            self.genre_ids[genre_id] = subgenre_ids

    def create_albums(self, album_count: int):
        """Create a specified number of fake albums and their related resources"""
        # On average an album will have between nine and 12 tracks
        track_counts = distribute(album_count * 10, album_count)
        # Generally an artist's legacy will be defined by their first five albums
        artist_counts = distribute(album_count // 5, album_count)
        # Force a new label for the first album
        label_id = None

        for artist_count, track_count in zip(artist_counts, track_counts):

            # Create a new label 30% of the time
            create_label = choices((False, True), weights=(70, 30), k=1)[0]
            if create_label or label_id is None:
                label = self.labels()
                label_id = label["id"]

            album = self.albums(label_id)
            album_artists = [self.artists() for _ in range(artist_count)]
            album_genres = sample(self.genre_ids.keys(), k=randint(1, 3))

            # Each track gets a related genre and artist from the album
            for _ in range(track_count):
                genre_id = choice(album_genres)
                subgenre_id = (
                    None
                    if not self.genre_ids[genre_id]
                    else choice(self.genre_ids[genre_id])
                )
                track = self.tracks(album["id"], genre_id, subgenre_id)

                # Setup join relationships for artists to tracks
                artist_ids = sample(
                    tuple(artist["id"] for artist in album_artists),
                    randint(1, len(album_artists)),
                )
                for artist_id in artist_ids:
                    self.artist_joins(artist_id, track["id"])

    def insert_data(self, batch_size: int):
        """Write any data in a related `IDObjectGenerator` to the database in batches."""
        session = self.session()
        while any((len(generator.data) != 0 for generator in self.generators)):
            for generator in self.generators:
                if not generator.data:
                    continue
                session.bulk_insert_mappings(
                    generator.schema_class, generator.data[:batch_size]
                )
                generator.data = generator.data[batch_size:]
                session.commit()

    def __call__(self, album_count: int, batch_size: int = 2000):
        """Create fake genre and album data in the database"""
        run_count = album_count // batch_size
        overflow = bool(album_count % batch_size)
        run_count = run_count + 1 if overflow else run_count

        self.create_genres()
        self.insert_data(batch_size)
        for _ in range(run_count):
            self.create_albums(batch_size)
            self.insert_data(batch_size)
