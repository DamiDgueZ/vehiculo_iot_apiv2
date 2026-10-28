import asyncio
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.encoders import jsonable_encoder

# Importaciones de tu nueva estructura modular
from app.models.schemas import (
    VehiculoCreateRequest, VehiculoUpdateRequest, ComandoCreateRequest,
    ComandoUpdateRequest, EstadoUpdateRequest, HistorialCreateRequest,
    DemoCreateRequest, DemoUpdateRequest, MovimientoDemoRequest,
    MovimientoIndividualRequest, DemoEjecucionRequest
)
from app.services.db_service import VehiculoIOTService
from app.websocket.websocket_manager import manager

app = FastAPI(title="Vehículo IoT API", version="1.0")

# Instanciamos el servicio (Programación Orientada a Objetos real)
servicio = VehiculoIOTService()

@app.get("/", tags=["General"])
def read_root():
    return {"message": "API de Retroexcavadora IoT activa y conectada a AWS RDS"}

@app.post("/vehiculos", tags=["Vehículos"])
def crear_vehiculo(data: VehiculoCreateRequest):
    try:
        id_vehiculo = servicio.crear_vehiculo(data.nombre, data.modelo, data.descripcion, data.microcontrolador)
        return {"status": "success", "id_vehiculo": id_vehiculo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehiculos", tags=["Vehículos"])
def get_vehiculos():
    return servicio.obtener_vehiculos()

@app.get("/vehiculos/{id_vehiculo}", tags=["Vehículos"])
def get_vehiculo_by_id(id_vehiculo: int):
    vehiculo = servicio.obtener_vehiculo(id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@app.put("/vehiculos/{id_vehiculo}", tags=["Vehículos"])
def actualizar_vehiculo(id_vehiculo: int, data: VehiculoUpdateRequest):
    try:
        servicio.actualizar_vehiculo(id_vehiculo, data.nombre, data.modelo, data.descripcion, data.microcontrolador, data.activo)
        return {"status": "success", "message": "Vehículo actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/vehiculos/{id_vehiculo}", tags=["Vehículos"])
def eliminar_vehiculo(id_vehiculo: int):
    try:
        servicio.eliminar_vehiculo(id_vehiculo)
        return {"status": "success", "message": "Vehículo eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vehiculos/{id_vehiculo}/comandos", tags=["Comandos"])
def crear_comando(id_vehiculo: int, data: ComandoCreateRequest):
    try:
        id_comando = servicio.crear_comando(id_vehiculo, data.nombre, data.codigo, data.descripcion)
        return {"status": "success", "id_comando": id_comando}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehiculos/{id_vehiculo}/comandos", tags=["Comandos"])
def get_comandos(id_vehiculo: int):
    comandos = servicio.obtener_comandos_vehiculo(id_vehiculo)
    return {"vehiculo_id": id_vehiculo, "comandos": comandos}

@app.put("/comandos/{id_comando}", tags=["Comandos"])
def actualizar_comando(id_comando: int, data: ComandoUpdateRequest):
    try:
        servicio.actualizar_comando(id_comando, data.nombre, data.codigo, data.descripcion, data.activo)
        return {"status": "success", "message": "Comando actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/comandos/{id_comando}", tags=["Comandos"])
def eliminar_comando(id_comando: int):
    try:
        servicio.eliminar_comando(id_comando)
        return {"status": "success", "message": "Comando eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehiculos/{id_vehiculo}/estado", tags=["Estado"])
def get_estado(id_vehiculo: int):
    estado = servicio.obtener_estado(id_vehiculo)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return {"vehiculo_id": id_vehiculo, "estado": estado}

@app.put("/vehiculos/{id_vehiculo}/estado", tags=["Estado"])
def actualizar_estado_vehiculo(id_vehiculo: int, data: EstadoUpdateRequest):
    try:
        servicio.actualizar_estado(id_vehiculo, data.id_comando_actual, data.conectado)
        return {"status": "success", "message": "Estado actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehiculos/{id_vehiculo}/historial", tags=["Historial"])
def get_historial(id_vehiculo: int):
    historial = servicio.obtener_historial(id_vehiculo)
    return {"vehiculo_id": id_vehiculo, "total_registros": len(historial), "historial": historial}

@app.post("/vehiculos/{id_vehiculo}/historial", tags=["Historial"])
def registrar_historial(id_vehiculo: int, data: HistorialCreateRequest):
    try:
        servicio.registrar_historial(id_vehiculo, data.id_comando, data.origen)
        return {"status": "success", "message": "Historial registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vehiculos/{id_vehiculo}/demos", tags=["DEMO"])
def crear_demo(id_vehiculo: int, data: DemoCreateRequest):
    try:
        id_demo = servicio.crear_demo(id_vehiculo, data.nombre, data.descripcion)
        return {"status": "success", "id_demo": id_demo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehiculos/{id_vehiculo}/demos", tags=["DEMO"])
def obtener_demos(id_vehiculo: int):
    demos = servicio.obtener_demos(id_vehiculo)
    return {"vehiculo_id": id_vehiculo, "demos": demos}

@app.put("/demos/{id_demo}", tags=["DEMO"])
def actualizar_demo(id_demo: int, data: DemoUpdateRequest):
    try:
        servicio.actualizar_demo(id_demo, data.nombre, data.descripcion, data.activo)
        return {"status": "success", "message": "Demo actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/demos/{id_demo}", tags=["DEMO"])
def eliminar_demo(id_demo: int):
    try:
        servicio.eliminar_demo(id_demo)
        return {"status": "success", "message": "Demo eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/demos/{id_demo}/movimientos", tags=["Movimientos DEMO"])
def agregar_movimiento_demo(id_demo: int, data: MovimientoDemoRequest):
    try:
        servicio.agregar_movimiento_demo(id_demo, data.id_comando, data.orden, data.duracion_ms, data.pausa_ms)
        return {"status": "success", "message": "Movimiento agregado a la demo"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demos/{id_demo}/movimientos", tags=["Movimientos DEMO"])
def get_movimientos_demo(id_demo: int):
    movs = servicio.obtener_movimientos_demo(id_demo)
    return {"id_demo": id_demo, "movimientos": movs}

@app.put("/demo-movimientos/{id_movimiento}", tags=["Movimientos DEMO"])
def actualizar_movimiento_demo(id_movimiento: int, data: MovimientoDemoRequest):
    try:
        servicio.actualizar_movimiento_demo(id_movimiento, data.id_comando, data.orden, data.duracion_ms, data.pausa_ms)
        return {"status": "success", "message": "Movimiento de demo actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/demo-movimientos/{id_movimiento}", tags=["Movimientos DEMO"])
def eliminar_movimiento_demo(id_movimiento: int):
    try:
        servicio.eliminar_movimiento_demo(id_movimiento)
        return {"status": "success", "message": "Movimiento de demo eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vehiculos/{id_vehiculo}/mover", tags=["Acciones en Tiempo Real"])
async def ejecutar_movimiento_individual(id_vehiculo: int, data: MovimientoIndividualRequest):
    vehiculo = servicio.obtener_vehiculo(id_vehiculo)
    if not vehiculo or not vehiculo.get("activo"):
        raise HTTPException(status_code=404, detail="Vehículo no encontrado o inactivo")

    comandos = servicio.obtener_comandos_vehiculo(id_vehiculo)
    comando_valido = next((c for c in comandos if c["id_comando"] == data.id_comando and c["activo"]), None)
    
    if not comando_valido:
        raise HTTPException(status_code=400, detail="El comando no existe o no pertenece a este vehículo")

    try:
        servicio.actualizar_estado(id_vehiculo=id_vehiculo, id_comando=data.id_comando, conectado=True)
        servicio.registrar_historial(id_vehiculo=id_vehiculo, id_comando=data.id_comando, origen=data.origen)

        evento_ws = {
            "evento": "movimiento_individual",
            "id_vehiculo": id_vehiculo,
            "comando": comando_valido["nombre"],
            "codigo": comando_valido["codigo"],
            "origen": data.origen
        }
        
        try:
            await manager.broadcast_to_vehicle(id_vehiculo, evento_ws)
        except Exception:
            pass

        return {"status": "success", "message": "Movimiento individual ejecutado y guardado en historial."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vehiculos/{id_vehiculo}/ejecutar-demo", tags=["Acciones en Tiempo Real"])
async def ejecutar_demo(id_vehiculo: int, data: DemoEjecucionRequest):
    movimientos = servicio.obtener_movimientos_demo(data.id_demo)
    if not movimientos:
        raise HTTPException(status_code=404, detail="La demo no existe o no tiene movimientos.")

    asyncio.create_task(reproducir_demo_ws(id_vehiculo, data.id_demo, movimientos))
    return {"status": "success", "message": f"Demo {data.id_demo} iniciada por WebSocket (sin afectar historial)."}

async def reproducir_demo_ws(id_vehiculo: int, id_demo: int, movimientos: list):
    try:
        await manager.broadcast_to_vehicle(id_vehiculo, {
            "evento": "inicio_demo",
            "id_vehiculo": id_vehiculo,
            "id_demo": id_demo
        })

        for mov in movimientos:
            servicio.actualizar_estado(id_vehiculo=id_vehiculo, id_comando=mov["id_comando"], conectado=True)

            await manager.broadcast_to_vehicle(id_vehiculo, {
                "evento": "paso_demo",
                "id_vehiculo": id_vehiculo,
                "orden": mov["orden"],
                "comando": mov["comando"],
                "codigo": mov["codigo"],
                "duracion_ms": mov["duracion_ms"],
                "pausa_ms": mov["pausa_ms"]
            })

            await asyncio.sleep(mov["duracion_ms"] / 1000.0)
            if mov["pausa_ms"] > 0:
                await asyncio.sleep(mov["pausa_ms"] / 1000.0)

        await manager.broadcast_to_vehicle(id_vehiculo, {
            "evento": "fin_demo",
            "id_vehiculo": id_vehiculo,
            "id_demo": id_demo
        })
    except Exception as e:
        print(f"Error reproduciendo demo por WebSocket: {e}")

@app.websocket("/ws/vehiculos/{id_vehiculo}")
async def websocket_endpoint(websocket: WebSocket, id_vehiculo: int):
    await manager.connect(id_vehiculo, websocket)
    try:
        estado_actual = servicio.obtener_estado(id_vehiculo)
        await websocket.send_json({"evento": "estado_inicial", "estado": jsonable_encoder(estado_actual)})

        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"Error en WebSocket: {e}")
        manager.disconnect(id_vehiculo, websocket)