from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

# Import database models
from database import Base, User, Device, WiFiNetwork, AccessLog, SessionActivity, AccessPolicy, AuditLog

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wifi_access.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="WiFi Access Monitoring System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models for request/response
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class DeviceCreate(BaseModel):
    name: str
    user_id: int

class DeviceResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WiFiNetworkCreate(BaseModel):
    ssid: str
    encryption_type: str

class WiFiNetworkResponse(BaseModel):
    id: int
    ssid: str
    encryption_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class AccessLogCreate(BaseModel):
    user_id: int
    wifi_network_id: int

class AccessLogResponse(BaseModel):
    id: int
    user_id: int
    wifi_network_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class SessionActivityCreate(BaseModel):
    user_id: int
    access_log_id: int

class SessionActivityResponse(BaseModel):
    id: int
    user_id: int
    access_log_id: int
    session_start: datetime
    session_end: Optional[datetime]

    class Config:
        from_attributes = True

class AuditLogCreate(BaseModel):
    action: str
    user_id: Optional[int] = None

class AuditLogResponse(BaseModel):
    id: int
    action: str
    timestamp: datetime
    user_id: Optional[int]

    class Config:
        from_attributes = True

# User Endpoints
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    audit = AuditLog(action=f"User created: {user.username}", user_id=new_user.id)
    db.add(audit)
    db.commit()
    
    return new_user

@app.get("/api/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    audit = AuditLog(action=f"User deleted: {user.username}")
    db.add(audit)
    db.commit()
    
    return {"message": "User deleted successfully"}

# Device Endpoints
@app.post("/api/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == device.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_device = Device(name=device.name, user_id=device.user_id)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    
    audit = AuditLog(action=f"Device registered: {device.name}", user_id=device.user_id)
    db.add(audit)
    db.commit()
    
    return new_device

@app.get("/api/devices", response_model=List[DeviceResponse])
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices

@app.get("/api/devices/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    
    audit = AuditLog(action=f"Device deleted: {device.name}")
    db.add(audit)
    db.commit()
    
    return {"message": "Device deleted successfully"}

# WiFi Network Endpoints
@app.post("/api/wifi-networks", response_model=WiFiNetworkResponse, status_code=status.HTTP_201_CREATED)
def create_wifi_network(network: WiFiNetworkCreate, db: Session = Depends(get_db)):
    db_network = db.query(WiFiNetwork).filter(WiFiNetwork.ssid == network.ssid).first()
    if db_network:
        raise HTTPException(status_code=400, detail="Network already exists")
    
    new_network = WiFiNetwork(ssid=network.ssid, encryption_type=network.encryption_type)
    db.add(new_network)
    db.commit()
    db.refresh(new_network)
    
    audit = AuditLog(action=f"WiFi network created: {network.ssid}")
    db.add(audit)
    db.commit()
    
    return new_network

@app.get("/api/wifi-networks", response_model=List[WiFiNetworkResponse])
def get_wifi_networks(db: Session = Depends(get_db)):
    networks = db.query(WiFiNetwork).all()
    return networks

@app.get("/api/wifi-networks/{network_id}", response_model=WiFiNetworkResponse)
def get_wifi_network(network_id: int, db: Session = Depends(get_db)):
    network = db.query(WiFiNetwork).filter(WiFiNetwork.id == network_id).first()
    if not network:
        raise HTTPException(status_code=404, detail="Network not found")
    return network

# Access Log Endpoints
@app.post("/api/access-logs", response_model=AccessLogResponse, status_code=status.HTTP_201_CREATED)
def log_access(log: AccessLogCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == log.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    network = db.query(WiFiNetwork).filter(WiFiNetwork.id == log.wifi_network_id).first()
    if not network:
        raise HTTPException(status_code=404, detail="Network not found")
    
    new_log = AccessLog(user_id=log.user_id, wifi_network_id=log.wifi_network_id)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    audit = AuditLog(action=f"WiFi access logged for user {user.username}", user_id=log.user_id)
    db.add(audit)
    db.commit()
    
    return new_log

@app.get("/api/access-logs", response_model=List[AccessLogResponse])
def get_access_logs(db: Session = Depends(get_db)):
    logs = db.query(AccessLog).all()
    return logs

@app.get("/api/access-logs/user/{user_id}", response_model=List[AccessLogResponse])
def get_user_access_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(AccessLog).filter(AccessLog.user_id == user_id).all()
    return logs

# Session Activity Endpoints
@app.post("/api/sessions", response_model=SessionActivityResponse, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionActivityCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_session = SessionActivity(user_id=session.user_id, access_log_id=session.access_log_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session

@app.get("/api/sessions", response_model=List[SessionActivityResponse])
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(SessionActivity).all()
    return sessions

@app.put("/api/sessions/{session_id}")
def end_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionActivity).filter(SessionActivity.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.session_end = datetime.utcnow()
    db.commit()
    
    return {"message": "Session ended"}

# Audit Log Endpoints
@app.get("/api/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).all()
    return logs

# Analytics Endpoints
@app.get("/api/analytics/user-activity/{user_id}")
def get_user_activity(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(AccessLog).filter(AccessLog.user_id == user_id).all()
    return {
        "user_id": user_id,
        "total_accesses": len(logs),
        "access_logs": logs
    }

@app.get("/api/analytics/network-usage/{network_id}")
def get_network_usage(network_id: int, db: Session = Depends(get_db)):
    logs = db.query(AccessLog).filter(AccessLog.wifi_network_id == network_id).all()
    return {
        "network_id": network_id,
        "total_accesses": len(logs),
        "access_logs": logs
    }

@app.get("/api/analytics/peak-hours")
def get_peak_hours(db: Session = Depends(get_db)):
    logs = db.query(AccessLog).all()
    hour_counts = {}
    for log in logs:
        hour = log.timestamp.hour
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    return {"peak_hours": hour_counts}

@app.get("/api/analytics/device-usage")
def get_device_usage(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    device_stats = []
    
    for device in devices:
        logs = db.query(AccessLog).all()
        device_stats.append({
            "device_id": device.id,
            "device_name": device.name,
            "user_id": device.user_id
        })
    
    return {"device_statistics": device_stats}

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "WiFi Access Monitoring System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)