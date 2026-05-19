from fastapi import APIRouter, HTTPException
from database import db
from schemas import TurmaCreate, TurmaUpdate

router = APIRouter(prefix="/turma", tags=["Turma"])

@router.post("/")
async def criar_turma(turma: TurmaCreate):
    nova = await db.turma.create(
    data={
        'nome': turma.nome,
        'semestre': turma.semestre,
        'id_sala': turma.id_sala
    }
)
    return nova

@router.get("/")
async def listar_turma():
    return await db.turma.find_many()

@router.put("/")
async def atualizar_turma(turma_id: int, dados: TurmaUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    
    try:
        turma_atualizado = await db.turma.update(
            where={'id': turma_id},
            data=dados_atualizar
        )
        return turma_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="Turma não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_turma(turma_id: int):
    try:
        turma_deletado = await db.turma.delete(where={'id': turma_id})
        return {"mensagem": "turma deletado com sucesso", "turma": turma_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Turma não encontrado")