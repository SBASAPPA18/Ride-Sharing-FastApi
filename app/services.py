import math
from typing import Optional

class Driver:
    def __init__(self, driver_id: int, x: float, y: float):
        self.driver_id = driver_id
        self.x = x
        self.y = y
        self.available = True

class Rider:
    def __init__(self, rider_id: int, x: float, y: float, dest_x: float, dest_y: float):
        self.rider_id = rider_id
        self.x = x
        self.y = y
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.matched_driver = None

class RideService:
    def __init__(self):
        self.drivers = {}
        self.riders = {}

    def add_driver(self, driver_id: int, x: float, y: float):
        self.drivers[driver_id] = Driver(driver_id, x, y)

    def add_rider(self, rider_id: int, x: float, y: float, dest_x: float, dest_y: float):
        self.riders[rider_id] = Rider(rider_id, x, y, dest_x, dest_y)

    def find_driver(self, rider_id: int) -> Optional[str]:
        rider = self.riders.get(rider_id)
        if not rider:
            return None
        
        closest_driver = None
        min_distance = float('inf')
        for driver in self.drivers.values():
            if driver.available:
                distance = self.calculate_distance(rider.x, rider.y, driver.x, driver.y)
                if distance <= 5 and distance < min_distance:
                    min_distance = distance
                    closest_driver = driver
        
        if closest_driver:
            rider.matched_driver = closest_driver
            closest_driver.available = False
            return f"Matched with Driver {closest_driver.driver_id}"
        return None

    def start_ride(self, rider_id: int) -> Optional[str]:
        rider = self.riders.get(rider_id)
        if not rider or not rider.matched_driver:
            return None
        
        return f"Ride started with Driver {rider.matched_driver.driver_id}"

    def complete_ride(self, rider_id: int) -> Optional[str]:
        rider = self.riders.get(rider_id)
        if not rider or not rider.matched_driver:
            return None
        
        distance = self.calculate_distance(rider.x, rider.y, rider.dest_x, rider.dest_y)
        bill = round(distance * 10, 2)
        rider.matched_driver.available = True
        rider.matched_driver = None
        return f"Ride completed. Bill: ${bill:.2f}"

    def cancel_ride(self, rider_id: int) -> Optional[str]:
        rider = self.riders.get(rider_id)
        if not rider or not rider.matched_driver:
            return None
        
        rider.matched_driver.available = True
        rider.matched_driver = None
        return f"Ride cancelled for Rider {rider_id}"

    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
