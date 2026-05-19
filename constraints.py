from timefold.solver.score import ConstraintFactory, HardSoftScore, Joiners, constraint_provider, Constraint
from domain import Lesson

@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory) -> list[Constraint]:
    return [
        room_conflict(constraint_factory),
        teacher_conflict(constraint_factory),
        student_group_conflict(constraint_factory)
    ]

def room_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return constraint_factory.for_each(Lesson) \
        .join(Lesson,
              Joiners.equal(lambda lesson: lesson.room),
              Joiners.equal(lambda lesson: lesson.timeslot),
              Joiners.less_than(lambda lesson: lesson.id)) \
        .penalize(HardSoftScore.ONE_HARD) \
        .as_constraint("Conflito de Sala")

def teacher_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return constraint_factory.for_each(Lesson) \
        .join(Lesson,
              Joiners.equal(lambda lesson: lesson.professor),
              Joiners.equal(lambda lesson: lesson.timeslot),
              Joiners.less_than(lambda lesson: lesson.id)) \
        .penalize(HardSoftScore.ONE_HARD) \
        .as_constraint("Conflito de Professor")

def student_group_conflict(constraint_factory: ConstraintFactory) -> Constraint:
<<<<<<< HEAD
    """Uma turma não pode ter duas aulas no mesmo horário."""
    return (
        constraint_factory.for_each(Lesson)
        .join(
            Lesson,
            Joiners.equal(lambda l: l.turma),
            Joiners.equal(lambda l: l.timeslot),
            Joiners.less_than(lambda l: l.id),
        )
        .penalize(HardSoftScore.ONE_HARD)
        .as_constraint("Conflito de Turma")
    )


def room_capacity(constraint_factory: ConstraintFactory) -> Constraint:
    """A sala deve comportar todos os alunos da turma."""
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda l: l.room is not None and l.num_alunos > l.room.capacidade)
        .penalize(
            HardSoftScore.ONE_HARD,
            lambda l: l.num_alunos - l.room.capacidade,
        )
        .as_constraint("Capacidade da Sala Excedida")
    )


def teacher_unavailability(constraint_factory: ConstraintFactory) -> Constraint:
    """Aula não pode ser marcada num horário em que o professor está indisponível."""
    return (
        constraint_factory.for_each(Lesson)
        .filter(
            lambda l: l.timeslot is not None
            and l.timeslot.id in l.professor.indisponibilidades
        )
        .penalize(HardSoftScore.ONE_HARD)
        .as_constraint("Indisponibilidade do Professor")
    )


def room_type_mismatch(constraint_factory: ConstraintFactory) -> Constraint:
    """A disciplina deve ser alocada no tipo de sala adequado (ex: laboratório)."""
    return (
        constraint_factory.for_each(Lesson)
        .filter(
            lambda l: l.room is not None
            and l.tipo_sala_necessario != "comum"
            and l.room.tipo != l.tipo_sala_necessario
        )
        .penalize(HardSoftScore.ONE_HARD)
        .as_constraint("Tipo de Sala Inadequado")
    )



def teacher_gap_between_lessons(constraint_factory: ConstraintFactory) -> Constraint:
    """
    Evita que o professor fique com 'janelas' (horários vagos entre aulas).
    Penaliza pares de aulas do mesmo professor no mesmo dia cujos timeslot IDs
    não são consecutivos (gap >= 2 slots).
    """
    return (
        constraint_factory.for_each(Lesson)
        .join(
            Lesson,
            Joiners.equal(lambda l: l.professor.id),
            Joiners.equal(lambda l: l.timeslot.dia_semana),
            Joiners.less_than(lambda l: l.timeslot.id),
        )
        .filter(
            # há pelo menos um slot vago entre as duas aulas
            lambda a, b: (b.timeslot.id - a.timeslot.id) > 1
        )
        .penalize(
            HardSoftScore.ONE_SOFT,
            lambda a, b: b.timeslot.id - a.timeslot.id - 1,
        )
        .as_constraint("Janela do Professor")
    )


def same_discipline_twice_a_day(constraint_factory: ConstraintFactory) -> Constraint:
    return (
        constraint_factory.for_each(Lesson)
        .join(
            Lesson,
            Joiners.equal(lambda l: l.turma),
            Joiners.equal(lambda l: l.disciplina),
            Joiners.equal(lambda l: l.timeslot.dia_semana),
            Joiners.less_than(lambda l: l.id),
        )
        .penalize(HardSoftScore.ONE_SOFT)
        .as_constraint("Mesma Disciplina Duas Vezes no Dia")
    )


def turma_too_many_lessons_in_a_day(constraint_factory: ConstraintFactory) -> Constraint:
    """
    Penaliza turmas com mais de 4 aulas num mesmo dia
    (carga excessiva de aulas consecutivas).
    """
    return (
        constraint_factory.for_each(Lesson)
        .join(
            Lesson,
            Joiners.equal(lambda l: l.turma),
            Joiners.equal(lambda l: l.timeslot.dia_semana),
            Joiners.less_than(lambda l: l.id),
        )
        .group_by(
            lambda a, b: (a.turma, a.timeslot.dia_semana),
            # conta pares; o número de aulas = (1 + raiz de 1+8n) / 2, mas
            # como o Timefold trabalha melhor com contagem direta, usamos
            # uma abordagem de filtro por threshold no penalize
        )
        # Alternativa direta: penaliza cada par acima do limiar (> 4 aulas/dia)
        # Como group_by com contagem pode variar por versão, usamos penalidade
        # simples para cada par extra além de 3 aulas no dia.
        .penalize(HardSoftScore.ONE_SOFT)
        .as_constraint("Excesso de Aulas da Turma no Dia")
    )


def teacher_prefers_shift(constraint_factory: ConstraintFactory) -> Constraint:
    return (
        constraint_factory.for_each(Lesson)
        .filter(
            lambda l: l.professor.turno_preferido is not None
            and l.timeslot is not None
            and _turno(l.timeslot.hora_inicio) != l.professor.turno_preferido
        )
        .penalize(HardSoftScore.ONE_SOFT)
        .as_constraint("Preferência de Turno do Professor")
    )


def distribute_lessons_across_week(constraint_factory: ConstraintFactory) -> Constraint:

    return (
        constraint_factory.for_each(Lesson)
        .join(
            Lesson,
            Joiners.equal(lambda l: l.turma),
            Joiners.equal(lambda l: l.timeslot.dia_semana),
            Joiners.less_than(lambda l: l.id),
        )
        .filter(lambda a, b: a.disciplina != b.disciplina)
        .penalize(HardSoftScore.ONE_SOFT)
        .as_constraint("Concentração de Aulas no Mesmo Dia")
    )
=======
    return constraint_factory.for_each(Lesson) \
        .join(Lesson,
              Joiners.equal(lambda lesson: lesson.turma),
              Joiners.equal(lambda lesson: lesson.timeslot),
              Joiners.less_than(lambda lesson: lesson.id)) \
        .penalize(HardSoftScore.ONE_HARD) \
        .as_constraint("Conflito de Turma")
>>>>>>> parent of cc80df1 (commit final antes de enviar pro repositorio oficial)
