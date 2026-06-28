
from pathlib import Path
import csv
from datetime import datetime


class DataLogger:
    def __init__(self, export_dir: Path):
        self.export_dir = export_dir
        self.csv_file = None
        self.csv_writer = None
        self.csv_path = None
        self.full_data = []
        self.timestep_counter = 0
        self.export_message = ""
        self.export_message_timer = 0

    def close_csv(self):
        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()
            self.csv_file.close()
        self.csv_file = None
        self.csv_writer = None

    def start_new_run(self):
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.close_csv()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = self.export_dir / f"simulation_run_{timestamp}.csv"
        self.csv_file = open(self.csv_path, "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file, delimiter=";")
        self.csv_writer.writerow(["Timestep", "Food", "Prey1", "Prey2", "Predators"])
        self.csv_file.flush()

        self.full_data = []
        self.timestep_counter = 0

        self.export_message = f"Nieuwe CSV: {self.csv_path.name}"
        self.export_message_timer = 180

    def log_step(self, food, prey1_count, prey2_count, predators):
        row = [
            self.timestep_counter,
            food,
            prey1_count,
            prey2_count,
            predators,
        ]
        self.full_data.append(row)

        if self.csv_writer is not None and self.csv_file is not None and not self.csv_file.closed:
            self.csv_writer.writerow(row)
            self.csv_file.flush()

        self.timestep_counter += 1
        return row

    def export_snapshot(self):
        self.export_dir.mkdir(parents=True, exist_ok=True)

        if self.csv_file is not None and not self.csv_file.closed:
            self.csv_file.flush()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.export_dir / f"simulation_full_export_{timestamp}_t{self.timestep_counter}.csv"

        with open(snapshot_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Timestep", "Food", "Prey1", "Prey2", "Predators"])
            writer.writerows(self.full_data)

        self.export_message = f"Volledige export: {snapshot_path.name}"
        self.export_message_timer = 180
        print(f"Volledige CSV-export gemaakt: {snapshot_path}")
        return snapshot_path.name