import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np


class ParkingLot:
    def __init__(self):
        self.parking_events = []
        self.df = None

    def generate_data(self):
        # Make 20 parking events
        for space_id in range(1, 21):
            # Random entry time between 8 AM and 5 PM today
            today = datetime(2025, 3, 16)
            start_time = today + timedelta(hours=8)  # 8 AM
            end_time = today + timedelta(hours=17)  # 5 PM

            # Generate random entry time
            time_range = (end_time - start_time).total_seconds()
            random_seconds = random.randint(0, int(time_range))
            entry_time = start_time + timedelta(seconds=random_seconds)

            # Random duration between 30-120 minutes
            duration_minutes = random.randint(30, 120)
            exit_time = entry_time + timedelta(minutes=duration_minutes)

            # Store as dictionary
            event = {
                "space_id": space_id,
                "entry_time": entry_time,
                "exit_time": exit_time
            }

            self.parking_events.append(event)

        # Convert to DataFrame
        df = pd.DataFrame(self.parking_events)

        # Save to CSV with your absolute path
        df.to_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv", index=False)

        return df

    def load_data(self):
        # Load CSV into self.df and convert time columns to datetime
        self.df = pd.read_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv")
        self.df['entry_time'] = pd.to_datetime(self.df['entry_time'])
        self.df['exit_time'] = pd.to_datetime(self.df['exit_time'])
        print(self.df)

    def calc_duration(self):
        # Calculate duration in hours
        self.df['duration'] = (self.df['exit_time'] - self.df['entry_time']).dt.total_seconds() / 3600

    def calc_fees(self):
        # Calculate fees: $2/hour, minimum $1
        self.df['fee'] = np.where(np.ceil(self.df['duration']) * 2 < 1, 1, np.ceil(self.df['duration']) * 2)
        # Save updated DataFrame to CSV
        self.df.to_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv", index=False)
        print(self.df)


# Create ParkingLot object and call methods
parking_lot = ParkingLot()
parking_lot.generate_data()
parking_lot.load_data()
parking_lot.calc_duration()
parking_lot.calc_fees()