from fastapi import FastAPI
from database import db
from rotas import professor, disciplina, sala, turma, horario, aula, otimizacao

app = FastAPI(title="API Sistema Acadêmico")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(professor.router)
app.include_router(disciplina.router)
app.include_router(sala.router)
app.include_router(turma.router)
app.include_router(horario.router)
app.include_router(aula.router)
app.include_router(otimizacao.router)
