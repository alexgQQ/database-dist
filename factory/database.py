from sqlalchemy import (Column, Date, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import (Session, declarative_base, relationship,
                            sessionmaker)

Base = declarative_base()


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    sub_genres = relationship("SubGenre", back_populates="genre")
    tracks = relationship("Track", back_populates="genre")


class SubGenre(Base):
    __tablename__ = "sub_genres"
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"))
    name = Column(String(100))

    genre = relationship("Genre", back_populates="sub_genres")
    tracks = relationship("Track", back_populates="sub_genre")


class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    albums = relationship("Album", back_populates="label")


class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey(f"{Label.__tablename__}.id"))
    name = Column(String(100))
    release_date = Column(Date)

    tracks = relationship("Track", back_populates="album")
    label = relationship("Label", back_populates="albums")


class ArtistTrackJoin(Base):
    __tablename__ = "artist_track_join"

    id = Column(Integer, primary_key=True)
    artist_id = Column(ForeignKey("artists.id"), primary_key=True)
    track_id = Column(ForeignKey("tracks.id"), primary_key=True)

    tracks = relationship("Track", back_populates="artists")
    artists = relationship("Artist", back_populates="tracks")


class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    tracks = relationship("ArtistTrackJoin", back_populates="artists")


class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey(f"{Album.__tablename__}.id"))
    genre_id = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"))
    sub_genre_id = Column(Integer, ForeignKey(f"{SubGenre.__tablename__}.id"))
    name = Column(String(100))
    length = Column(Float(precision=2))

    album = relationship("Album", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    sub_genre = relationship("SubGenre", back_populates="tracks")

    artists = relationship("ArtistTrackJoin", back_populates="tracks")


def init_db(
    db_type: str, user: str, password: str, host: str, database: str
) -> Session:
    """
    Setup database connection and return a session pool"""
    if db_type == "sqlite":
        db_url = "sqlite://"
    else:
        db_url = f"{db_type}://{user}:{password}@{host}/{database}"
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def delete_data():
    """Delete all data entries"""
    Album.query().delete()
    Artist.query().delete()
    ArtistTrackJoin.query().delete()
    Label.query().delete()
    Genre.query().delete()
    SubGenre.query().delete()
    Track.query().delete()
