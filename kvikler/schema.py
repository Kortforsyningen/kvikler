from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint

import geoalchemy2

import kvikler

if kvikler.IS_TESTING:
    # In testing mode we create the tables in a local sqlite database which doesn't support schemas
    Base = declarative_base()
else:
    Base = declarative_base(metadata=MetaData(schema=kvikler.schema))

class CoordinateSystem(Base):
    __tablename__ = 'coordinatesystems'

    id = Column(Integer, primary_key=True)

class Coordinate(Base):
    __tablename__ = 'coordinates'

    id = Column(Integer, primary_key=True)
    point = Column(Integer, ForeignKey('points.id'))
    crs = Column(Integer, ForeignKey('coordinatesystems.id'))

class Elevation(Base):
    __tablename__ = 'elevations'

    id = Column(Integer, primary_key=True)
    point = Column(Integer, ForeignKey('points.id'))
    crs = Column(Integer, ForeignKey('coordinatesystems.id'))

class Point(Base):
    __tablename__ = 'points'

    #columns
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('pointgroups.id'))
    type_id = Column(Integer, ForeignKey('pointtypes.id'))

    # relationships
    coordinates = relationship(Coordinate, backref='coordinate')
    elevations = relationship(Coordinate, backref='elevation')

class PointType(Base):
    __tablename__ = 'pointtypes'

    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # relationsships
    points = relationship(Point, backref='type')

class PointGroup(Base):
    __tablename__ ='pointgroups'

    # columns
    id = Column(Integer, primary_key=True)

    # relationships
    points = relationship(Point, backref='group')

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)

class Observation(Base):
    __tablename__ = 'observations'

    # columns
    id = Column(Integer, primary_key=True)
    from_point = Column(Integer, ForeignKey('points.id'))
    to_point = Column(Integer, ForeignKey('points.id'))
    campaign = Column(Integer, ForeignKey('campaigns.id'))

    # relationships

    # constraints
    points_not_equal = CheckConstraint('from_point != to_point')

def create_schema(engine):
    Base.metadata.create_all(engine)


def drop_schema(engine):
    Base.metadata.drop_all(engine)
