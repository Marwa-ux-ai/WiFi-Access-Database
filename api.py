from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Dummy data
users = []  # user data will hold user info
devices = []  # device management
access_logs = []  # access logging
analytics_data = []  # analytics info
network_management_data = []  # network management info
audit_logs = []  # audit logs

class User(BaseModel):
    username: str
    password: str

class Device(BaseModel):
    device_id: str
    user: str
    status: str

class AccessLog(BaseModel):
    user: str
    device_id: str
    timestamp: str

@app.post("/register/")
async def register(user: User):
    if any(u.username == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already registered")
    users.append(user)
    return user

@app.post("/login/")
async def login(user: User):
    if any(u.username == user.username and u.password == user.password for u in users):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/devices/")
async def add_device(device: Device):
    devices.append(device)
    return device

@app.get("/devices/", response_model=List[Device])
async def get_devices():
    return devices

@app.post("/access_logs/")
async def log_access(log: AccessLog):
    access_logs.append(log)
    return log

@app.get("/analytics/", response_model=List[AccessLog])
async def get_analytics():
    return analytics_data

@app.get("/network_management/")
async def manage_network():
    return network_management_data

@app.get("/audit_logs/")
async def get_audit_logs():
    return audit_logs
