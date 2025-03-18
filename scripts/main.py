import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np
import matplotlib.pyplot as plt


class ParkingLot:
    def __init__(self):
        self.parking_events = []
        self.df = None

    def generate_data(self):
        # Make 20 parking events
        for space_id in range(1, 21):
            today = datetime(2025, 3, 16)
            start_time = today + timedelta(hours=8)  # 8 AM
            end_time = today + timedelta(hours=17)  # 5 PM
            time_range = (end_time - start_time).total_seconds()
            random_seconds = random.randint(0, int(time_range))
            entry_time = start_time + timedelta(seconds=random_seconds)
            duration_minutes = random.randint(30, 120)
            exit_time = entry_time + timedelta(minutes=duration_minutes)
            event = {
                "space_id": space_id,
                "entry_time": entry_time,
                "exit_time": exit_time
            }
            self.parking_events.append(event)
        df = pd.DataFrame(self.parking_events)
        df.to_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv", index=False)
        return df

    def load_data(self):
        # Load CSV and convert times to datetime
        self.df = pd.read_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv")
        self.df['entry_time'] = pd.to_datetime(self.df['entry_time'])
        self.df['exit_time'] = pd.to_datetime(self.df['exit_time'])

    def calc_duration(self):
        # Calculate duration in hours
        self.df['duration'] = (self.df['exit_time'] - self.df['entry_time']).dt.total_seconds() / 3600

    def calc_fees(self):
        # Calculate fees: $2/hour, minimum $1
        self.df['fee'] = np.where(np.ceil(self.df['duration']) * 2 < 1, 1, np.ceil(self.df['duration']) * 2)
        self.df.to_csv("/Users/piyushu/PMS/ParkingManagementSystem/data/parking_data.csv", index=False)

    def check_availability(self, check_time):
        # Check occupied spaces at a given time
        check_time = pd.to_datetime(check_time)
        occupied = self.df[(self.df['entry_time'] <= check_time) & (self.df['exit_time'] > check_time)]['space_id'].count()
        available = 20 - occupied
        print(f"At {check_time}: {occupied} occupied, {available} available")
        return occupied, available

    def generate_report(self):
        # Daily report: revenue, usage, peak hour
        total_revenue = self.df['fee'].sum()
        total_usage = len(self.df)
        peak_hour = self.df['entry_time'].dt.hour.mode()[0]
        report = pd.DataFrame({
            "Total Revenue": [total_revenue],
            "Total Usage": [total_usage],
            "Peak Hour": [peak_hour]
        })
        report.to_csv("/Users/piyushu/PMS/ParkingManagementSystem/reports/daily_report.csv", index=False)
        print(report)

    def plot_occupancy(self):
        # Plot occupancy by hour
        hours = range(8, 18)  # 8 AM to 5 PM
        occupancy = []
        for hour in hours:
            time = datetime(2025, 3, 16, hour)
            occupied = self.df[(self.df['entry_time'] <= time) & (self.df['exit_time'] > time)]['space_id'].count()
            occupancy.append(occupied)
        plt.bar(hours, occupancy)
        plt.xlabel("Hour of Day")
        plt.ylabel("Occupied Spaces")
        plt.title("Parking Occupancy by Hour")
        plt.savefig("/Users/piyushu/PMS/ParkingManagementSystem/visuals/occupancy.png")
        plt.close()


# Run everything
parking_lot = ParkingLot()
parking_lot.generate_data()
parking_lot.load_data()
parking_lot.calc_duration()
parking_lot.calc_fees()
parking_lot.check_availability("2025-03-16 12:00:00")
parking_lot.generate_report()
parking_lot.plot_occupancy()