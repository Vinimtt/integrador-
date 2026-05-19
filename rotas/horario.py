from fastapi import APIRouter, HTTPException
from database import db
from schemas import HorarioCreate, HorarioUpdate

router = APIRouter(prefix="/horario", tags=["Horario"])

@router.post("/")
async def criar_horario(horario: HorarioCreate):
    nova = await db.horario.create(
        data={
            'dia_semana': horario.dia_semana,
            'horario_inicio': horario.horario_inicio,
            'horario_fim': horario.horario_fim
        }

    )
    return nova

@router.get("/")
async def listar_horarios():
    return await db.horario.find_many()


@router.put("/")
async def atualizar_horario(horario_id: int, dados: HorarioUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    try:
        horario_atualizado = await db.horario.update(
            where={'id': horario_id},
            data=dados_atualizar
        )
        return horario_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="Horario não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_horario(horario_id: int):
    try:
        horario_deletado = await db.horario.delete(where={'id': horario_id})
        return {"mensagem": "horario deletado com sucesso", "horario": horario_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Horario não encontrado")