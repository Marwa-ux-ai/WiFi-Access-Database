-- SQL Schema for WiFi Access Database

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE devices (
    device_id INT PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(100) NOT NULL,
    mac_address VARCHAR(17) NOT NULL UNIQUE,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_devices_user_id ON devices(user_id);

CREATE TABLE wifi_networks (
    network_id INT PRIMARY KEY AUTO_INCREMENT,
    ssid VARCHAR(100) NOT NULL,
    password VARCHAR(255),
    security_protocol VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE access_logs (
    access_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    device_id INT,
    network_id INT,
    access_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (network_id) REFERENCES wifi_networks(network_id)
);

CREATE INDEX idx_access_logs_user_id ON access_logs(user_id);

CREATE TABLE session_activities (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    logout_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_session_activities_user_id ON session_activities(user_id);

CREATE TABLE access_policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    policy_name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);