"""Database ORM models for SQLAlchemy."""

from sqlalchemy import create_engine, Engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

import sys
sys.path.append('../../../')

from backend.core.domain.models import Aluno

class DatabaseSession:
    """Database session class for SQLAlchemy. It creates a database engine
    and a session. The engine is used to create the database tables and
    the session is used to query the database. The engine and session
    are passed to the repositories.\\
    """
    def __init__(self):
        """Initializes the database engine and session."""
        # postgresql://<username>:<password>@<host>:<port>/<database_name>
        self.engine = create_engine(
            'postgresql://postgres:postgres@172.18.0.2:5432/postgres',
            echo=True)

        self.db_session = Session(bind=self.engine)

    def get_db_session(self) -> Session:
        """Returns the SQLAlchemy session."""
        return self.db_session

    def close_db_session(self):
        """Closes the database session."""
        self.db_session.close()

    def get_engine(self) -> Engine:
        """Returns the SQLAlchemy engine."""
        return self.engine


Base = declarative_base()

class AlunoORM(Base):
    """Aluno ORM class for SQLAlchemy."""
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    born_date = Column(Date, nullable=False)
    address = Column(String(200), nullable=False)
    tutor_name = Column(String(100), nullable=False)
    tutor_phone = Column(String(20), nullable=False)
    class_shift = Column(String(20), nullable=False)

    @staticmethod
    def from_aluno(aluno):
        """Converts an Aluno object to an AlunoORM object."""
        return AlunoORM(
            name=aluno.name,
            born_date=aluno.born_date,
            address=aluno.address,
            tutor_name=aluno.tutor_name,
            tutor_phone=aluno.tutor_phone,
            class_shift=aluno.class_shift
        )

    @staticmethod
    def to_aluno(aluno_orm):
        """Converts an AlunoORM object to an Aluno object."""
        return Aluno(
            id=aluno_orm.id,
            name=aluno_orm.name,
            born_date=aluno_orm.born_date,
            address=aluno_orm.address,
            tutor_name=aluno_orm.tutor_name,
            tutor_phone=aluno_orm.tutor_phone,
            class_shift=aluno_orm.class_shift
        )


class ProfessorORM(Base):
    """Professor ORM class for SQLAlchemy."""
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @staticmethod
    def from_professor(professor):
        """Converts a Professor object to a ProfessorORM object."""
        return ProfessorORM(
            name=professor.name,
            email=professor.email,
            password=professor.password
        )


class PeriodoLetivoORM(Base):
    """PeriodoLetivo ORM class for SQLAlchemy."""
    __tablename__ = 'periodo_letivo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    class_shift = Column(String(100), nullable=False)
    dias_sem_aula = relationship("DiaSemAulaORM", backref="periodo_letivo")


class DiaSemAulaORM(Base):
    """DiaSemAula ORM class for SQLAlchemy."""
    __tablename__ = 'dia_sem_aula'

    id = Column(Integer, primary_key=True, autoincrement=True)
    periodo_letivo_id = Column(Integer, ForeignKey('periodo_letivo.id'), nullable=False)
    date = Column(Date, nullable=False)
    reason = Column(String(100), nullable=False)


def create_tables(engine: Engine):
    """Creates the database tables."""
    Base.metadata.create_all(engine)


def create_some_alunos(engine: Engine):
    """Creates some Aluno objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    aluno_list = [
        {'name': 'João Silva', 'born_date': '2000-01-01',
         'address': 'Rua Principal, 123', 'tutor_name': 'Maria Silva',
         'tutor_phone': '(11) 5555-5555', 'class_shift': 'Manhã'},
        {'name': 'Maria Silva', 'born_date': '2001-02-02',
         'address': 'Rua das Flores, 456', 'tutor_name': 'João Silva',
         'tutor_phone': '(11) 5555-5555', 'class_shift': 'Tarde'},
        {'name': 'Roberto Santos', 'born_date': '2002-03-03',
         'address': 'Rua dos Pinheiros, 789', 'tutor_name': 'Alice Santos',
         'tutor_phone': '(11) 5555-5555', 'class_shift': 'Manhã'},
        {'name': 'Samantha Oliveira', 'born_date': '2003-04-04',
         'address': 'Rua das Palmeiras, 321', 'tutor_name': 'Miguel Oliveira',
         'tutor_phone': '(11) 5555-5555', 'class_shift': 'Tarde'}
    ]

    for aluno in aluno_list:
        new_aluno = AlunoORM(name=aluno['name'], born_date=aluno['born_date'],
                             address=aluno['address'], tutor_name=aluno['tutor_name'],
                             tutor_phone=aluno['tutor_phone'], class_shift=aluno['class_shift'])

        existing_aluno = session.query(AlunoORM).filter_by(name=new_aluno.name, born_date=new_aluno.born_date).first()
        if existing_aluno: # avoid duplicates and errors for existing data
            continue

        # Insert a new student
        session.add(new_aluno)
        session.commit()


def create_some_professor(engine: Engine):
    """Creates some Professor objects and saves it to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    professor_list = [
        {'name': 'William', 'email': 'william@bhzconnection.org.br',
        'password': 'password123'}
    ]
    for professor in professor_list:
        new_professor = ProfessorORM(name=professor['name'],
                                     email=professor['email'],
                                     password=professor['password'])

        existing_professor = session.query(ProfessorORM).filter_by(email=new_professor.email).first()
        if existing_professor: # avoid duplicates and errors for existing data
            continue

        # Insert a new professor
        session.add(new_professor)
        session.commit()

def delete_all_alunos(engine: Engine):
    """Deletes all Aluno objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all alunos
    session.query(AlunoORM).delete()
    session.commit()


def delete_all_professors(engine: Engine):
    """Deletes all Professor objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all professors
    session.query(ProfessorORM).delete()
    session.commit()


def create_some_periodos_letivos(engine: Engine):
    """Creates some PeriodoLetivo objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    periodo_letivo_list = [
        {'start_date': '2023-01-01', 'end_date': '2023-06-30', 'class_shift': 'Manhã'},
    ]

    for periodo_letivo in periodo_letivo_list:
        new_periodo_letivo = PeriodoLetivoORM(start_date=periodo_letivo['start_date'],
                                              end_date=periodo_letivo['end_date'],
                                              class_shift=periodo_letivo['class_shift'])

        existing_periodo_letivo = session.query(PeriodoLetivoORM).filter_by(start_date=new_periodo_letivo.start_date, end_date=new_periodo_letivo.end_date).first()
        if existing_periodo_letivo: # avoid duplicates and errors for existing data
            continue

        # Insert a new periodo letivo
        session.add(new_periodo_letivo)
        session.commit()


def create_some_dias_sem_aula(engine: Engine):
    """Creates some DiaSemAula objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    dia_sem_aula_list = [
        {'periodo_letivo_id': 1, 'date': '2023-01-01', 'reason': 'Feriado'},
        {'periodo_letivo_id': 1, 'date': '2023-01-02', 'reason': 'Feriado'},
        {'periodo_letivo_id': 1, 'date': '2023-01-03', 'reason': 'Feriado'},
    ]

    for dia_sem_aula in dia_sem_aula_list:
        new_dia_sem_aula = DiaSemAulaORM(periodo_letivo_id=dia_sem_aula['periodo_letivo_id'],
                                        date=dia_sem_aula['date'],
                                        reason=dia_sem_aula['reason'])

        existing_dia_sem_aula = session.query(DiaSemAulaORM).filter_by(periodo_letivo_id=new_dia_sem_aula.periodo_letivo_id, date=new_dia_sem_aula.date, reason=new_dia_sem_aula.reason).first()
        if existing_dia_sem_aula: # avoid duplicates and errors for existing data
            continue

        # Insert a new dia sem aula
        session.add(new_dia_sem_aula)
        session.commit()


def delete_all_periodos_letivos(engine: Engine):
    """Deletes all PeriodoLetivo objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all periodos letivos
    session.query(PeriodoLetivoORM).delete()
    session.commit()

def delete_all_dias_sem_aula(engine: Engine):
    """Deletes all DiaSemAula objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all dias sem aula
    session.query(DiaSemAulaORM).delete()
    session.commit()
