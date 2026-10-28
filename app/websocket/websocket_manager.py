from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, vehicle_id: int, websocket: WebSocket):
        await websocket.accept()
        if vehicle_id not in self.active_connections:
            self.active_connections[vehicle_id] = []
        self.active_connections[vehicle_id].append(websocket)

    def disconnect(self, vehicle_id: int, websocket: WebSocket):
        if vehicle_id in self.active_connections:
            if websocket in self.active_connections[vehicle_id]:
                self.active_connections[vehicle_id].remove(websocket)
            if not self.active_connections[vehicle_id]:
                del self.active_connections[vehicle_id]

    async def broadcast_to_vehicle(self, vehicle_id: int, message: dict):
        if vehicle_id in self.active_connections:
            for connection in list(self.active_connections[vehicle_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(vehicle_id, connection)

# Creamos la instancia para usarla en main.py
manager = ConnectionManager()