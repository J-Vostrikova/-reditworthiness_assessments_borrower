import sqlite3
from datetime import datetime
import json

class DecisionDatabase:
    def __init__(self, db_path='credit_decisions.db'):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()
    
    def _initialize_db(self):
        """Инициализация базы данных"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_data TEXT,
                decision TEXT,
                probability REAL,
                risk_level TEXT,
                interest_rate TEXT,
                credit_limit TEXT,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()
    
    def store_decision(self, client_data, decision):
        """Сохранение решения в базу данных"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO credit_decisions 
            (client_data, decision, probability, risk_level, interest_rate, credit_limit, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            json.dumps(client_data),
            decision['decision'],
            decision['probability'],
            decision['risk_level'],
            decision['interest_rate'],
            decision['limit'],
            datetime.now()
        ))
        self.conn.commit()
    
    def get_recent_decisions(self, limit=10):
        """Получение последних решений"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM credit_decisions 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()

# Миграция на PostgreSQL (Задача 3.2)
class Database:
    def __init__(self):
        self.engine = create_engine('postgresql://user:pass@localhost:5432/credits')  # Новый движок БД

    def migrate_from_sqlite(self, sqlite_path):
        """Перенос данных из старой БД"""
        old_db = sqlite3.connect(sqlite_path)
        old_data = pd.read_sql('SELECT * FROM decisions', old_db)
        old_data.to_sql('decisions', self.engine, if_exists='replace')