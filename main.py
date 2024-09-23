from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import extract
from pydantic import BaseModel
from datetime import date, datetime

app = FastAPI()

#initialize db
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer)
    room_reservation_id = Column(String)
    night_of_stay = Column(Date)
    event_timestamp = Column(DateTime)
    status = Column(Integer)
    
Base.metadata.create_all(engine)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

class BookingSerializer(BaseModel):
    id:int
    hotel_id:int
    room_reservation_id:str
    night_of_stay:date
    event_timestamp:datetime
    status:int
    
class BookingCreateSerializer(BookingSerializer):
    pass

#endpoints
@app.get("/")
async def read_root():
    return {"Welcome": "Hotel Industry"}

@app.get("/events/",response_model = List[BookingSerializer])
async def get_events(db: Session = Depends(get_db)):
    return db.query(Booking).order_by(Booking.event_timestamp.asc()).limit(100).all()

@app.get("/events/{hotel_id}", response_model=List[BookingSerializer])
async def get_event_by_hotel(db: Session = Depends(get_db), hotel_id:int=0, status:int|None=None,
        room_reservation_id: str|None=None, night_of_stay:date|None=None, event_timestamp:date|None=None):
    print(hotel_id)
    qry ={"hotel_id": hotel_id}
      
    if status is not None:
        qry["status"] = status
    if room_reservation_id is not None:
        qry["room_reservation_id"] = room_reservation_id
    if night_of_stay is not None:
        qry["night_of_stay"] = night_of_stay
    if event_timestamp is not None:
        qry["event_timestamp"] = event_timestamp
        
    booking = db.query(Booking).filter_by(**qry).all()
    if booking is None:
        raise HTTPException(status_code=404, detail="Not found")

    return booking

@app.post("/events/", response_model=BookingSerializer)
async def create_event(booking:BookingSerializer, db: Session = Depends(get_db)):
    new_booking =  Booking(**booking.model_dump())

    db.add(new_booking)
    db.commit()
    db.add(new_booking)
    return new_booking

@app.get("/dashboard/{hotel_id}")
async def get_event_by_hotel(db: Session = Depends(get_db), hotel_id:int=0, year:int=2021,
        monthly: bool=False):
    print(hotel_id)
    dash = {}
    if monthly:
        dash = db.query(extract('month', Booking.event_timestamp), func.count('*')).filter(extract('year',Booking.event_timestamp)==year).group_by(extract('month', Booking.event_timestamp))
    else:
        dash = db.query(extract('day', Booking.event_timestamp), func.count('*')).filter(extract('year',Booking.event_timestamp)==year).group_by(extract('day', Booking.event_timestamp))
    return dash