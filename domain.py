from timefold.solver.domain import (
    planning_entity, planning_solution, PlanningId, PlanningVariable, 
    PlanningEntityCollectionProperty, ProblemFactCollectionProperty, ValueRangeProvider, PlanningScore
)
from timefold.solver.score import HardSoftScore
from dataclasses import dataclass, field
from typing import Annotated

@dataclass
class Timeslot:
    id: int
    dia_semana: str
    hora_inicio: str
    hora_fim: str

@dataclass
class Room:
    id: int
    numero: str
    capacidade: int

@planning_entity
@dataclass
class Lesson:
    id: Annotated[int, PlanningId]
<<<<<<< HEAD
    professor: Professor          
=======
    professor: str
>>>>>>> parent of cc80df1 (commit final antes de enviar pro repositorio oficial)
    disciplina: str
    turma: str
    timeslot: Annotated[Timeslot | None, PlanningVariable] = field(default=None)
    room: Annotated[Room | None, PlanningVariable] = field(default=None)

@planning_solution
@dataclass
class Timetable:
    timeslots: Annotated[list[Timeslot], ProblemFactCollectionProperty, ValueRangeProvider]
    rooms: Annotated[list[Room], ProblemFactCollectionProperty, ValueRangeProvider]
    lessons: Annotated[list[Lesson], PlanningEntityCollectionProperty]
    score: Annotated[HardSoftScore | None, PlanningScore] = field(default=None)