#!/usr/bin/env python3
"""
Project: Deception-Based Cyber Attack Detection and Analysis using Honeypots
Component: Database Schema Handler
Student Name: Thandra Shishira | Student ID: B23CN126
"""

import sqlite3
import time

class HoneypotDatabase:
    def __init__(self, db_name="honeypot_telemetry.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create table for credential logs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                password TEXT,
                status TEXT
            )
        ''')
        # Create table for quarantined payload drops
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payload_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                file_name TEXT,
                sha256_hash TEXT,
                source_url TEXT
            )
        ''')
        self.conn.commit()

    def log_auth(self, username, password, status="ACCEPTED"):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.cursor.execute("INSERT INTO auth_logs (timestamp, username, password, status) VALUES (?, ?, ?, ?)",
                            (t, username, password, status))
        self.conn.commit()

if __name__ == "__main__":
    db = HoneypotDatabase()
    db.log_auth("root", "password123")
    print("[+] Database SQLite structures initialized successfully.")
