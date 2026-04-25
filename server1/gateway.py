import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import websockets
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# --- Database Setup (Placeholder) ---
# Replace with actual credentials if needed. For testing without a live PostgreSQL DB, 
# it defaults to a local SQLite file so you don't get 'Connection refused' errors!
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./omnivision.db")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)

    class HazardReport(Base):
        __tablename__ = "hazard_reports"
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, index=True)
        lat = Column(Float)
        lng = Column(Float)
        hazard_type = Column(String, index=True)
        timestamp = Column(DateTime, default=datetime.utcnow)

    # In production, use Alembic for migrations instead of create_all
    Base.metadata.create_all(bind=engine)
    print(f"[DB] Successfully connected to database: {DATABASE_URL}")
except Exception as e:
    print(f"[DB WARN] Could not connect to Database. Error: {e}")

# --- FastAPI App Setup ---
app = FastAPI(title="Server 1: API Gateway (WebSocket Proxy)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER_2_IP = os.getenv("SERVER_2_IP", "192.168.0.44")
SERVER_2_WS_URL = f"ws://{SERVER_2_IP}:8001/internal/stream"

@app.websocket("/api/stream")
async def websocket_proxy(client_ws: WebSocket):
    """
    Proxies WebSocket connections from the React Native app to Server 2.
    """
    await client_ws.accept()
    print(f"[Gateway] Accepted connection from mobile app.")

    try:
        async with websockets.connect(SERVER_2_WS_URL) as server2_ws:
            print(f"[Gateway] Successfully connected to Server 2 at {SERVER_2_WS_URL}")

            # Loop 1: Mobile App -> Server 2 (Forwarding Frames)
            async def forward_to_server2():
                try:
                    while True:
                        # Assuming mobile app sends binary frame data
                        data = await client_ws.receive_bytes()
                        await server2_ws.send(data)
                except WebSocketDisconnect:
                    print("[Gateway] Mobile app disconnected (Forwarding -> S2).")
                except Exception as e:
                    print(f"[Gateway] Error reading from mobile: {e}")

            # Loop 2: Server 2 -> Mobile App (Forwarding JSON results)
            async def forward_to_mobile():
                try:
                    while True:
                        # Assuming Server 2 sends JSON payload responses (alerts/audio)
                        data = await server2_ws.recv()
                        await client_ws.send_text(data)
                except websockets.exceptions.ConnectionClosed:
                    print("[Gateway] Server 2 disconnected (Forwarding -> Mobile).")
                except Exception as e:
                    print(f"[Gateway] Error reading from Server 2: {e}")

            # Run both bi-directional loops concurrently
            # gather() allows both loops to run simultaneously. If one fails/exits, the other continues 
            # until the websocket is closed. We can use return_exceptions=True to prevent full crashes.
            await asyncio.gather(
                forward_to_server2(),
                forward_to_mobile(),
                return_exceptions=True
            )
            
    except websockets.exceptions.WebSocketException as e:
        print(f"[Gateway] Failed to connect to Server 2: {e}")
        try:
            await client_ws.close(code=1011, reason="Server 2 unreachable")
        except:
            pass
    except Exception as e:
        print(f"[Gateway] Unexpected proxy error: {e}")
        try:
            await client_ws.close(code=1011, reason="Internal gateway error")
        except:
            pass
    finally:
        print("[Gateway] Proxy session ended.")

if __name__ == "__main__":
    import uvicorn
    # Bound to port 8002 to avoid conflicting with your actively running main.py on 8000
    uvicorn.run("gateway:app", host="0.0.0.0", port=8002, reload=True)
