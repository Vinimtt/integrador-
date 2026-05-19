from fastapi import APIRouter, HTTPException
from database import db
from schemas import ProfessorCreate, ProfessorUpdate

router = APIRouter(prefix="/professor", tags=["Professor"])

@router.post("/")
async def criar_professor(professor: ProfessorCreate):
    nova = await db.professor.create(
    data={
        'nome': professor.nome,
        'email': professor.email,
        'disponibilidade': professor.disponibilidade
    }
)
    return nova

@router.get("/")
async def listar_professores():
    return await db.professor.find_many()

@router.put("/")
async def atualizar_professor(professor_id: int, dados: ProfessorUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    try:
        professor_atualizado = await db.professor.update(
            where={'id': professor_id},
            data=dados_atualizar
        )
        return professor_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="Professor não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_professor(professor_id: int):
    try:
        professor_deletado = await db.professor.delete(where={'id': professor_id})
        return {"mensagem": "professor deletado com sucesso", "professor": professor_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Professor não encontrado")