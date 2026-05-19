from fastapi import APIRouter
from prisma import Prisma
from domain import Timetable, Lesson, Room, Timeslot
from constraints import define_constraints
from timefold.solver import SolverFactory
from timefold.solver.config import SolverConfig, TerminationConfig, ScoreDirectorFactoryConfig, Duration

router = APIRouter(prefix="/otimizacao", tags=["Otimização"])
db = Prisma()

@router.post("/gerar-grade")
async def gerar_grade():
    if not db.is_connected():
        await db.connect()

    db_rooms = await db.sala.find_many()
    db_timeslots = await db.horario.find_many()
    db_lessons = await db.aula.find_many(include={'professor': True, 'turma': True, 'disciplina': True})

<<<<<<< HEAD
    rooms = [
        Room(
            id=r.id,
            numero=r.numero,
            capacidade=r.capacidade,
            tipo=getattr(r, 'tipo', 'comum'),
        )
        for r in db_rooms
    ]

    timeslots = [
        Timeslot(
            id=t.id,
            dia_semana=t.dia_semana,
            hora_inicio=t.horario_inicio,
            hora_fim=t.horario_fim,
        )
        for t in db_timeslots
    ]

    timeslot_id_set = {t.id for t in timeslots}

    professores_cache: dict[int, Professor] = {}
    for l in db_lessons:
        p = l.professor
        if p.id not in professores_cache:
            # indisponibilidades esperadas como lista de IDs de horário no campo
            # disponibilidade do banco; se vier em outro formato, adapte aqui
            raw_indisp = getattr(p, 'indisponibilidades', None) or []
            indisp = [i for i in raw_indisp if i in timeslot_id_set]

            professores_cache[p.id] = Professor(
                id=p.id,
                nome=p.nome,
                email=p.email,
                indisponibilidades=indisp,
                turno_preferido=getattr(p, 'turno_preferido', None),
            )

    lessons = [
        Lesson(
            id=l.id,
            professor=professores_cache[l.professor.id],
            disciplina=l.disciplina.nome,
            turma=l.turma.nome,
            num_alunos=getattr(l.turma, 'num_alunos', 0),
            tipo_sala_necessario=getattr(l.disciplina, 'tipo_sala_necessario', 'comum'),
        )
        for l in db_lessons
    ]
=======
    rooms = [Room(r.id, r.numero, r.capacidade) for r in db_rooms]
    timeslots = [Timeslot(t.id, t.dia_semana, t.horario_inicio, t.horario_fim) for t in db_timeslots]
    lessons = [Lesson(l.id, l.professor.nome, l.disciplina.nome, l.turma.nome) for l in db_lessons]
>>>>>>> parent of cc80df1 (commit final antes de enviar pro repositorio oficial)

    solver_config = SolverConfig(
        solution_class=Timetable,
        entity_class_list=[Lesson],
        score_director_factory_config=ScoreDirectorFactoryConfig(
            constraint_provider_function=define_constraints
        ),
        termination_config=TerminationConfig(spent_limit=Duration(seconds=10))
    )

    solver = SolverFactory.create(solver_config).build_solver()

    problem = Timetable(timeslots, rooms, lessons)
    solution = solver.solve(problem)

    for lesson in solution.lessons:
        if lesson.timeslot and lesson.room:
            await db.aula.update(
                where={'id': lesson.id},
                data={'id_horario': lesson.timeslot.id, 'id_sala': lesson.room.id}
            )

    return {"status": "Grade gerada com sucesso", "score": str(solution.score)}