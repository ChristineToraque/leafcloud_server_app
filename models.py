from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    plant_id = Column(String, index=True)
    lettuce_image_url = Column(String)

    # Sensor Data
    ec = Column(Float)
    ph = Column(Float)
    temp_c = Column(Float)

    # Prediction Data
    n_ppm = Column(Float)
    p_ppm = Column(Float)
    k_ppm = Column(Float)