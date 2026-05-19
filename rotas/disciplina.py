from fastapi import APIRouter, HTTPException
from database import db
from schemas import DisciplinaCreate, DisciplinaUpdate

router = APIRouter(prefix="/disciplina", tags=["Disciplina"])

@router.post("/")
async def criar_disciplina(disciplina: DisciplinaCreate):
    nova = await db.disciplina.create(
        data={
            'nome': disciplina.nome,
            'codigo': disciplina.codigo,
            'carga_horaria': disciplina.carga_horaria,
            'periodo_recomendado': disciplina.periodo_recomendado

        }

    )
    return nova

@router.get("/")
async def listar_disciplinas():
    return await db.disciplina.find_many()


@router.put("/")
async def atualizar_disciplina(disciplina_id: int, dados: DisciplinaUpdate):
    dados_atualizar = dados.dict(exclude_unset=True)
    try:
        disciplina_atualizado = await db.disciplina.update(
            where={'id': disciplina_id},
            data=dados_atualizar
        )
        return disciplina_atualizado
    except Exception:
        raise HTTPException(status_code=404, detail="disciplina não encontrada ou erro ao atualizar")

@router.delete("/")
async def deletar_disciplina(disciplina_id: int):
    try:
        disciplina_deletado = await db.disciplina.delete(where={'id': disciplina_id})
        return {"mensagem": "Disciplina deletado com sucesso", "disciplina": disciplina_deletado}
    except Exception:
        raise HTTPException(status_code=404, detail="Disciplina não encontrado")