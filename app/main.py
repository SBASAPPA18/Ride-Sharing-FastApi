from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .services import RideService

app = FastAPI()
ride_service = RideService()

class Driver(BaseModel):
    driver_id: int
    x: float
    y: float

class Rider(BaseModel):
    rider_id: int
    x: float
    y: float
    dest_x: float
    dest_y: float

class StartRideRequest(BaseModel):
    rider_id: int

class CompleteRideRequest(BaseModel):
    rider_id: int

@app.post("/add_driver/")
async def add_driver(driver: Driver):
    ride_service.add_driver(driver.driver_id, driver.x, driver.y)
    return {"message": f"Driver {driver.driver_id} added at ({driver.x}, {driver.y})"}

@app.post("/add_rider/")
async def add_rider(rider: Rider):
    ride_service.add_rider(rider.rider_id, rider.x, rider.y, rider.dest_x, rider.dest_y)
    return {"message": f"Rider {rider.rider_id} added at ({rider.x}, {rider.y}), destination ({rider.dest_x}, {rider.dest_y})"}

@app.post("/match_driver/")
async def match_driver(rider_id: int):
    result = ride_service.find_driver(rider_id)
    if result:
        return {"message": result}
    else:
        raise HTTPException(status_code=404, detail="No driver found within 5 km range.")

@app.post("/start_ride/")
async def start_ride(request: StartRideRequest):
    result = ride_service.start_ride(request.rider_id)
    if result:
        return {"message": result}
    else:
        raise HTTPException(status_code=404, detail="Cannot start ride. No matched driver.")

@app.post("/complete_ride/")
async def complete_ride(request: CompleteRideRequest):
    result = ride_service.complete_ride(request.rider_id)
    if result:
        return {"message": result}
    else:
        raise HTTPException(status_code=404, detail="Cannot complete ride. No matched driver.")

@app.post("/cancel_ride/")
async def cancel_ride(rider_id: int):
    result = ride_service.cancel_ride(rider_id)
    if result:
        return {"message": result}
    else:
        raise HTTPException(status_code=404, detail="Ride cannot be cancelled. No matched driver.")
