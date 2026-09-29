import sqlite3
import json


class History:
    def __init__(self, database_path="netdiag.db"):
        self.database_path = database_path
        self.connection = sqlite3.connect(self.database_path)

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                success INTEGER NOT NULL,
                message TEXT NOT NULL,
                duration REAL NOT NULL,
                details TEXT,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                problem TEXT NOT NULL,
                severity TEXT NOT NULL,
                cause TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            )
            """
        )

        self.connection.commit()

    def create_run(self, timestamp):
        cursor = self.connection.execute(
            """
            INSERT INTO runs (timestamp)
            VALUES (?)
            """,
            (timestamp,)
        )

        self.connection.commit()

        return cursor.lastrowid

    def add_check(self, run_id, result):
        details = (
            json.dumps(result.details)
            if result.details is not None
            else None
        )

        self.connection.execute(
            """
            INSERT INTO checks (
                run_id,
                name,
                success,
                message,
                duration,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                result.name,
                int(result.success),
                result.message,
                result.duration,
                details
            )
        )

        self.connection.commit()

    def add_diagnosis(self, run_id, diagnosis):
        recommendations = json.dumps(diagnosis.recommendations)

        self.connection.execute(
            """
            INSERT INTO diagnoses (
                run_id,
                problem,
                severity,
                cause,
                recommendations
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                run_id,
                diagnosis.problem,
                diagnosis.severity,
                diagnosis.cause,
                recommendations
            )
        )

        self.connection.commit()

    def get_runs(self, limit=10):
        cursor = self.connection.execute(
            """
            SELECT id, timestamp
            FROM runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    def get_run_diagnoses(self, run_id):
        cursor = self.connection.execute(
            """
            SELECT problem, severity, cause
            FROM diagnoses
            WHERE run_id = ?
            """,
            (run_id,)
        )

        return cursor.fetchall()




    def close(self):
        self.connection.close()