from pydantic import BaseModel
from typing import Optional

class ProfessorCreate(BaseModel):
    nome: str
    email: str
    disponibilidade: bool

class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    disponibilidade: Optional[bool] = None

class DisciplinaCreate(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int
    periodo_recomendado: int

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    carga_horaria: Optional[int] = None
    periodo_recomendado: Optional[int] = None

class SalaCreate(BaseModel):
    numero: str
    capacidade: int
    recursos: str

class SalaUpdate(BaseModel):
    numero: Optional[str] = None
    capacidade: Optional[int] = None
    recursos: Optional[str] = None

class TurmaCreate(BaseModel):
    nome: str
    semestre: str
    id_sala: int

class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    semestre: Optional[str] = None
    id_sala: Optional[int] = None

class HorarioCreate(BaseModel):
    dia_semana: str
    horario_inicio: str
    horario_fim: str

class HorarioUpdate(BaseModel):
    dia_semana: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fim: Optional[str] = None

class AulaCreate(BaseModel):
    id_turma: int
    id_disciplina: int
    id_professor: int

class AulaUpdate(BaseModel):
    id_turma: Optional[int] = None
    id_disciplina: Optional[int] = None
    id_professor: Optional[int] = None


