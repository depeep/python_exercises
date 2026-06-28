import sqlite3
from pathlib import Path
from datetime import datetime



class SnapshotEngine:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        self._create_tables()

    # ==================================================
    # DATABASE SETUP
    # ==================================================
    def _create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestep INTEGER,
            created_at TEXT
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            type TEXT,
            x REAL,
            y REAL,
            energy REAL,
            age INTEGER,
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
        )
        """)

        self.conn.commit()

    # ==================================================
    # SAVE SNAPSHOT
    # ==================================================
    def save(self, game):
        self.cur.execute(
            "INSERT INTO snapshots (timestep, created_at) VALUES (?, ?)",
            (game.logger.timestep_counter, datetime.now().isoformat())
        )

        snapshot_id = self.cur.lastrowid

        # FOOD
        for f in game.foodPopulation:
            self._insert_entity(snapshot_id, "food", f.position, None, f.age)

        # PREY
        for p in game.preyPopulation:
            self._insert_entity(snapshot_id, "prey", p.position, p.energy, p.age)

        # PREY2
        for p in game.prey2Population:
            self._insert_entity(snapshot_id, "prey2", p.position, p.energy, p.age)

        # PREDATOR
        for pr in game.predatorPopulation:
            self._insert_entity(snapshot_id, "predator", pr.position, pr.energy, pr.age)

        self.conn.commit()
        return snapshot_id

    def _insert_entity(self, snapshot_id, etype, pos, energy, age):
        self.cur.execute("""
        INSERT INTO entities (snapshot_id, type, x, y, energy, age)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            snapshot_id,
            etype,
            pos[0],
            pos[1],
            energy,
            age
        ))

    # ==================================================
    # LOAD SNAPSHOT
    # ==================================================
    def load(self, game, snapshot_id):
        self.cur.execute("""
            SELECT type, x, y, energy, age
            FROM entities
            WHERE snapshot_id = ?
        """, (snapshot_id,))
        
        rows = self.cur.fetchall()

        # reset game state
        game.preyPopulation.clear()
        game.prey2Population.clear()
        game.predatorPopulation.clear()
        game.foodPopulation.clear()

        # rebuild entities
        for etype, x, y, energy, age in rows:

            if etype == "food":
                obj = game.factory.spawnFood() or game.foodPopulation[-1]
                obj = game.foodPopulation[-1]
                obj.position = [x, y]
                obj.age = age

            elif etype == "prey":
                game.factory.spawnPrey()
                obj = game.preyPopulation[-1]
                obj.position = [x, y]
                obj.energy = energy
                obj.age = age

            elif etype == "prey2":
                game.factory.spawnPrey2()
                obj = game.prey2Population[-1]
                obj.position = [x, y]
                obj.energy = energy
                obj.age = age

            elif etype == "predator":
                game.factory.spawnPredator()
                obj = game.predatorPopulation[-1]
                obj.position = [x, y]
                obj.energy = energy
                obj.age = age

    # ==================================================
    # HELPERS
    # ==================================================
    def list_snapshots(self):
        self.cur.execute("SELECT id, timestep FROM snapshots ORDER BY id")
        return self.cur.fetchall()

    def get_latest_snapshot_id(self):
        self.cur.execute("SELECT MAX(id) FROM snapshots")
        row = self.cur.fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()