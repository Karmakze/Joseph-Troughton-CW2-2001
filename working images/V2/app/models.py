from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import db
from datetime import datetime


class Country(db.Model):
    __tablename__ = 'Country'
    __table_args__ = {'schema': 'CW2'}
    
    Country_ID = Column(Integer, primary_key=True, autoincrement=True)
    Country_Name = Column(String(256), nullable=False)


class County(db.Model):
    __tablename__ = 'County'
    __table_args__ = {'schema': 'CW2'}
    
    County_ID = Column(Integer, primary_key=True, autoincrement=True)
    County_Name = Column(String(256), nullable=False)
    County_Country_ID = Column(Integer, ForeignKey('CW2.Country.Country_ID', ondelete='CASCADE'), nullable=False)

    country = relationship("Country", backref="counties")


class City(db.Model):
    __tablename__ = 'City'
    __table_args__ = {'schema': 'CW2'}

    City_ID = Column(Integer, primary_key=True, autoincrement=True)
    City_Name = Column(String(256), nullable=False)
    City_County_ID = Column(Integer, ForeignKey('CW2.County.County_ID', ondelete='CASCADE'), nullable=False)

    county = relationship("County", backref="cities")


class Tags(db.Model):
    __tablename__ = 'Tags'
    __table_args__ = {'schema': 'CW2'}

    Tag_ID = Column(Integer, primary_key=True, autoincrement=True)
    Tag_Name = Column(String(128), nullable=False, unique=True)


class Trail(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}

    Trail_ID = Column(Integer, primary_key=True, autoincrement=True)
    Trail_Name = Column(String(128), nullable=False)
    Trail_Description = Column(String(512))
    Trail_Type = Column(String(25))
    Trail_Difficulty = Column(String(10))
    Trail_Distance = Column(Numeric(10, 2))
    Trail_Elevation_Gain = Column(Numeric(6, 1))
    Trail_Length = Column(Integer)
    Trail_Rating = Column(Numeric(2, 1))
    Trail_City_ID = Column(Integer, ForeignKey('CW2.City.City_ID', ondelete='CASCADE'), nullable=False)
    Trail_Creator = Column(Integer, ForeignKey('CW2.Users.User_ID', ondelete='CASCADE'), nullable=False)

    city = relationship("City", backref="trails")
    creator = relationship("Users", backref="created_trails")


class TrailAddLog(db.Model):
    __tablename__ = 'TrailAddLog'
    __table_args__ = {'schema': 'CW2'}
    
    Log_ID = Column(Integer, primary_key=True, autoincrement=True)
    User_ID = Column(Integer, ForeignKey('CW2.Users.User_ID', ondelete='SET NULL'))
    Trail_ID = Column(Integer, ForeignKey('CW2.Trails.Trail_ID', ondelete='SET NULL'))
    Added_Timestamp = Column(DateTime, default=datetime.utcnow)

    trail = relationship("Trail", backref="trail_logs")
    user = relationship("Users", backref="trail_logs")


class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}

    User_ID = Column(Integer, primary_key=True, autoincrement=True)
    User_Email = Column(String(320), nullable=False)
    User_Name = Column(String(128), nullable=False, unique=True)
    User_City_ID = Column(Integer, ForeignKey('CW2.City.City_ID', ondelete='SET NULL'))

    city = relationship("City", backref="residents")


class UserTrails(db.Model):
    __tablename__ = 'UserTrails'
    __table_args__ = {'schema': 'CW2'}

    User_ID = Column(Integer, ForeignKey('CW2.Users.User_ID', ondelete='CASCADE'), primary_key=True)
    Trail_ID = Column(Integer, ForeignKey('CW2.Trails.Trail_ID', ondelete='CASCADE'), primary_key=True)


class UserTrailsTags(db.Model):
    __tablename__ = 'UserTrailsTags'
    __table_args__ = {'schema': 'CW2'}

    User_ID = Column(Integer, ForeignKey('CW2.Users.User_ID', ondelete='CASCADE'), primary_key=True)
    Trail_ID = Column(Integer, ForeignKey('CW2.Trails.Trail_ID', ondelete='CASCADE'), primary_key=True)
    Tag_ID = Column(Integer, ForeignKey('CW2.Tags.Tag_ID', ondelete='CASCADE'), primary_key=True)

    __table_args__ = (
        UniqueConstraint('User_ID', 'Trail_ID', 'Tag_ID', name='UQ_UserTrailTag'),
    )
