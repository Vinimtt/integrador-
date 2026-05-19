from fastapi import APIRouter, HTTPException
from database import db
from schemas import AulaCreate, AulaUpdate

router = APIRouter(prefix="/aula", tags=["Aula"])

@router.post("/")
async def criar_aula(aula: AulaCreate):
    nova = await db.aula.create(
        data={
            'id_turma': aula.id_turma,
            'id_disciplina': aula.id_disciplina,
            'id_professor': aula.id_professor
        }

    )
    return nova

@router.get("/")
async def listar_aulas():
    return await db.aula.find_many()


@router.put("/")
async def atualizar_aula(aula_id: int, dados: AulaUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    try:
        aula_atualizado = await db.aula.update(
            where={'id': aula_id},
            data=dados_atualizar
        )
        return aula_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="aula não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_aula(aula_id: int):
    try:
        aula_deletado = await db.aula.delete(where={'id': aula_id})
        return {"mensagem": "Aula deletado com sucesso", "aula": aula_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Aula não encontrado")