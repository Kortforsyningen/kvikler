# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
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
    name = Column(String, unique=True, nullable=False)
    horizontal = Column(Boolean)
    vertical = Column(Boolean)
    proj_init_id = Column(String, unique=True, nullable=False)

class Coordinate(Base):
    __tablename__ = 'coordinates'

    id = Column(Integer, primary_key=True)
    point_id = Column(Integer, ForeignKey('points.id'))
    calc_id = Column(Integer, ForeignKey('calculations.id'))
    crs_id = Column(Integer, ForeignKey('coordinatesystems.id'))
    x = Column(Numeric(30, 15), nullable=False)
    y = Column(Numeric(30, 15), nullable=False)

    measured = Column(Boolean)

class Elevation(Base):
    __tablename__ = 'elevations'

    id = Column(Integer, primary_key=True)
    point_id = Column(Integer, ForeignKey('points.id'))
    calc_id = Column(Integer, ForeignKey('calculations.id'))
    crs_id = Column(Integer, ForeignKey('coordinatesystems.id'))

    elevation = Column(Numeric(30, 15), nullable=False)
    mean_error = Column(Float) # aposteriori variance
    obs_time = Column(DateTime)
    pub_time = Column(Date)



class Point(Base):
    __tablename__ = 'points'

    #columns
    id = Column(Integer, primary_key=True)
    primary_ident_id = Column(Integer, ForeignKey('idents.id', use_alter=True))

    # Not all of these should be able to co-exist.
    # TODO: Constraints need to be added based on rules we need to decide on.
    plane = Column(Boolean)
    height = Column(Boolean)
    gps = Column(Boolean)
    jessen = Column(Boolean)
    natural = Column(Boolean)
    pedestal = Column(Boolean) # "postament", sikkert oversat forkert
    discontinued = Column(Boolean) # "tabtgået"
    fundamental = Column(Boolean) # "fundamentalpunkt"
    support = Column(Boolean) # "hjælpepunkt"
    maintained = Column(Boolean) # by SDFE

    remarks = Column(String)

class IdentType(Base):
    __tablename__ = 'identtypes'

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    description = Column(String)


class Ident(Base):
    __tablename__ = 'idents'

    #columns
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('identtypes.id'))
    point_id = Column(Integer, ForeignKey('points.id'))
    name = Column(String, unique=True)


class Network(Base):
    __tablename__ = 'networks'

    # columns
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))

    name = Column(String)

class NetworkPoint(Base):
    __tablename__ = 'network_points'

    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey('networks.id'))
    point_id = Column(Integer, ForeignKey('points.id'))

    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime)

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)

    start_date = Column(Date, nullable=False)
    stop_date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, CheckConstraint('LENGTH(description)>200'), nullable=False)

class Calculation(Base):
    __tablename__ = 'calculations'

    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey('networks.id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))

    description = Column(String)
    calculation_time = Column(DateTime)

class HeightTimeSerie(Base):
    __tablename__ = 'heighttimeseries'

    id = Column(Integer, primary_key=True)
    calc_id = Column(Integer, ForeignKey('calculations.id'))
    fixed_point = Column(Integer, ForeignKey('points.id'))


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    standard_comment = Column(Boolean)

class ObservationMethod(Base):
    __tablename__ = 'observationmethods'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    descr = Column(String)

class Observation(Base):
    __tablename__ = 'observations'
    __table_args__ = (
            CheckConstraint('from_id != to_id', name='non_equal_points'),
    )

    # columns
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey('points.id'))
    to_id = Column(Integer, ForeignKey('points.id'))
    obs_method_id = Column(Integer, ForeignKey('observationmethods.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    campaign = Column(Integer, ForeignKey('campaigns.id'))

    obs_time = Column(DateTime)

    sum_elev_dif = Column(Float)
    sum_dist = Column(Float)

    n_setup = Column(Integer)# opstilling
    apriori = Column(Float)
    centering = Column(Float)
    variance_estimate = Column(Float)

    withheld = Column(Boolean)
    replaces_or_replaced_by = Column(Integer) # Er den her nødvendigt?


    # relationships

    # constraints

def create_schema(engine):
    Base.metadata.create_all(engine)


def drop_schema(engine):
    Base.metadata.drop_all(engine)
