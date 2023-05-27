import os
from sqlalchemy import Boolean, Column, DateTime, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

database_path = os.getenv('DATABASE_LINK_URL') 
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

"""
Movies
"""
class Movies (db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title  = Column(String)
    release_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    is_delete = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow())

    # def __init__(self, title, release_date):
    #     self.title = title
    #     self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.is_delete = True
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

"""
Actors
"""
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    is_delete = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow())

    # def __init__(self, name, age, gender):
    #     self.name = name,
    #     self.age = age,
    #     self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.is_delete = True
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
