import math
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import get_db, UserLocation, Pothole, Alert

router = APIRouter(tags=["Geo-Memory"])

class LocationUpdate(BaseModel):
    user_id: int
    lat: float
    lng: float

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth's surface
    using the Haversine formula. Returns distance in meters.
    """
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.post("/api/location/update")
async def update_location(payload: LocationUpdate, db: Session = Depends(get_db)):
    """
    Receives continuous location updates, logs them, and checks for nearby hazards within 50 meters.
    Implements a 5-minute cooldown to prevent spamming the user for the same pothole.
    """
    # 1. Log the user's current location
    new_loc = UserLocation(
        user_id=payload.user_id,
        latitude=payload.lat,
        longitude=payload.lng
    )
    db.add(new_loc)
    db.commit()

    # 2. Query active hazards
    # In a production environment with millions of hazards, use PostGIS or a bounding box filter here.
    # For now, we fetch all potholes.
    potholes = db.query(Pothole).all()
    
    generated_alerts = []
    current_time = datetime.utcnow()
    cooldown_threshold = current_time - timedelta(minutes=5)

    for ph in potholes:
        if ph.latitude is None or ph.longitude is None:
            continue
            
        # 3. Calculate distance
        distance = calculate_distance(payload.lat, payload.lng, ph.latitude, ph.longitude)
        
        if distance <= 50.0:
            # 4. Cooldown Check: Has this user been alerted about this pothole in the last 5 minutes?
            recent_alert = db.query(Alert).filter(
                Alert.user_id == payload.user_id,
                Alert.pothole_id == ph.pothole_id,
                Alert.alert_time >= cooldown_threshold
            ).first()
            
            if not recent_alert:
                # 5. Insert new alert record and prepare payload
                alert_msg = f"Warning: Severe pothole {int(distance)} meters away."
                
                new_alert = Alert(
                    user_id=payload.user_id,
                    pothole_id=ph.pothole_id,
                    distance_meters=distance,
                    alert_message=alert_msg
                )
                db.add(new_alert)
                db.commit()
                db.refresh(new_alert)
                
                generated_alerts.append({
                    "pothole_id": ph.pothole_id,
                    "distance_meters": round(distance, 1),
                    "alert_message": alert_msg
                })

    return {
        "status": "success",
        "alerts": generated_alerts
    }
