from fastapi import FastAPI
from .routes.users import router_users
from .routes.tickets import router_tickets

app = FastAPI(title="FlowDesk")

app.include_router(router_users) 
app.include_router(router_tickets)

@app.get("/")
async def root():
    return {"message": "Sistema de Tickets API", "version": "1.0.0"}