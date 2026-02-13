from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

def init_db(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    devices = relationship('Device', backref='user')

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_name = Column(String)

class WiFiNetwork(Base):
    __tablename__ = 'wifi_networks'
    id = Column(Integer, primary_key=True)
    ssid = Column(String, unique=True)
    password = Column(String)

class AccessLog(Base):
    __tablename__ = 'access_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    network_id = Column(Integer, ForeignKey('wifi_networks.id'))
    access_time = Column(DateTime)

class SessionActivity(Base):
    __tablename__ = 'session_activities'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_start = Column(DateTime)
    session_end = Column(DateTime)

class AccessPolicy(Base):
    __tablename__ = 'access_policies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    policy_name = Column(String)
    is_active = Column(Boolean)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    log_entry = Column(String)
    created_at = Column(DateTime)
