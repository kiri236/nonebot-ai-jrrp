import os
import sqlite3
from .constant import DATA_DIR
from typing import Dict, Union, Optional
from datetime import datetime
class DataBase:
    def __init__(self,name:str):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.conn = sqlite3.connect(os.path.join(DATA_DIR,f"{name}.db"))
        self.cur = self.conn.cursor()
    def create_database(self):
        init_daily_luck_text = '''CREATE TABLE IF NOT EXISTS fortune_daily
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT,
            date DATE,
            jrrp TEXT,
            tips TEXT);'''
        init_luck_act_text = '''CREATE TABLE IF NOT EXISTS fortune_details
           (name TEXT,
            daily_id INTEGER NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('宜', '忌')),
            activity TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (daily_id) REFERENCES fortune_daily(id));'''
        self.cur.execute(init_daily_luck_text)
        self.cur.execute(init_luck_act_text)
        self.conn.commit()
    def insert(self,data:Dict):
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.cur.execute('''
                INSERT INTO fortune_daily (name,date, jrrp, tips)
                VALUES (?, ?, ?, ?)
            ''', (data["name"],date, data["今日运势"], data["tips"]))
            daily_id = self.cur.lastrowid
            for activity,desc in data["宜"].items():
                self.cur.execute("""
                INSERT INTO fortune_details (daily_id, category, activity, description)
                VALUES (?, '宜', ?, ?)
                """, (daily_id, activity, desc))
            for activity,desc in data["忌"].items():
                self.cur.execute("""
                INSERT INTO fortune_details (daily_id, category, activity, description)
                VALUES (?, '忌', ?, ?)
                """, (daily_id, activity, desc))
            self.conn.commit()
            print("ok")
            return daily_id
        except Exception as  e:
            self.conn.rollback()
            print("err")
            return None
    def query(self,name:str,date:str)->Union[Union[Optional[Dict], int]]:
        try:
            self.cur.execute("""
            SELECT id,jrrp,tips
            FROM fortune_daily
            WHERE name = ? AND date = ?
            """,(name,date))

            record = self.cur.fetchone()
            if not record:
                return 0
            id,jrrp,tips = record
            result = {
                "name":name,
                "date":date,
                "今日运势":jrrp,
                "tips":tips,
                "宜":{},
                "忌":{}
            }
            self.cur.execute("""
            SELECT activity, description 
            FROM fortune_details 
            WHERE daily_id = ? AND category = '宜'
            """,(id,))
            for activity,desc in self.cur.fetchall():
                result["宜"][activity] = desc
            self.cur.execute("""
                        SELECT activity, description 
                        FROM fortune_details 
                        WHERE daily_id = ? AND category = '忌'
                        """, (id,))
            for activity,desc in self.cur.fetchall():
                result["忌"][activity] = desc
            return result
        except Exception as e:
            print("err")
            return None
    def __del__(self):
        self.conn.close()