from fastapi import APIRouter, HTTPException
from database import db
from schemas import SalaCreate, SalaUpdate

router = APIRouter(prefix="/sala", tags=["Sala"])

@router.post("/")
async def criar_sala(sala: SalaCreate):
    nova = await db.sala.create(
    data={
        'numero': sala.numero,
        'capacidade': sala.capacidade,
        'recursos': sala.recursos
    }
)
    return nova

@router.get("/")
async def listar_sala():
    return await db.sala.find_many()

@router.put("/")
async def atualizar_sala(sala_id: int, dados: SalaUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    try:
        sala_atualizado = await db.sala.update(
            where={'id': sala_id},
            data=dados_atualizar
        )
        return sala_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="Sala não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_sala(sala_id: int):
    try:
        sala_deletado = await db.sala.delete(where={'id': sala_id})
        return {"mensagem": "sala deletado com sucesso", "sala": sala_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Sala não encontrado")
    