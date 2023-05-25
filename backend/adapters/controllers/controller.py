"""This module implements the controller classes to enable the communication
between the frontend adapter and the domain layer without exposing the
database adapter to the frontend adapter.
"""

from backend.core.domain.services import AlunoService, ProfessorService
from backend.adapters.database.repositories import (
    AlunoRepositoryPostgres, ProfessorRepositoryPostgres,
    SQLAlchemySession
)


class AlunoController:
    """Aluno controller class for adapters. It provides methods for
    creating, updating, and retrieving Aluno objects. It takes a db object,
    an AlunoRepository object, and an AlunoService object as dependencies.\\
    This class enables the communication between the frontend adapter and
    the domain layer, without exposing the database adapter to the
    frontend adapter.
    """
    def __init__(self) -> None:
        """Initializes the controller with a db object, an AlunoRepository
        object, and an AlunoService object."""
        database = SQLAlchemySession()
        self.database_session = database.get_db_session()
        self.aluno_repository = AlunoRepositoryPostgres(self.database_session)
        self.aluno_service = AlunoService(self.aluno_repository)


    def get_alunos_by_name(self, name):
        """Retrieves a list of Aluno objects from the repository by name."""
        return self.aluno_service.get_alunos_by_name(name)
        # return True


    def create(self, name, born_date, address, tutor_name,
                    tutor_phone, class_shift):
        """Creates a new Aluno object and saves it to the repository."""
        return self.aluno_service.create_aluno(name, born_date, address,
                                               tutor_name, tutor_phone,
                                               class_shift)
        # return True

    def update(self, aluno_id, name=None, born_date=None,
                        address=None, tutor_name=None, tutor_phone=None,
                        class_shift=None):
        """Updates an existing Aluno object and saves it to the repository."""
        return self.aluno_service.update_aluno(aluno_id, name, born_date,
                       address, tutor_name, tutor_phone,
                       class_shift)
        # return True

    def remove(self, aluno_id):
        """Removes an existing Aluno object from the repository."""
        return self.aluno_service.remove_aluno(aluno_id)
        # return True


class ProfessorController:
    """Professor controller class for adapters. It provides methods for
    creating, updating, and retrieving Professor objects. It takes a db object,
    an ProfessorRepository object, and an ProfessorService object as dependencies.\\
    This class enables the communication between the frontend adapter and
    the domain layer, without exposing the database adapter to the
    frontend adapter.
    """
    def __init__(self,) -> None:
        """Initializes the controller with a db object, an ProfessorRepository
        object, and an ProfessorService object."""
        database = SQLAlchemySession()
        self.database_session = database.get_db_session()
        self.professor_repository = ProfessorRepositoryPostgres(self.database_session)
        self.professor_service = ProfessorService(self.professor_repository)

    def login(self, email, password):
        """Verifies professor login credentials."""
        print(email, password) # TODO: Remove later
        self.professor_service.login(email, password)
        # return True

    def create(self, name, email, password):
        """Creates a new Professor object and saves it to the repository."""
        return self.professor_service.create_professor(name, email, password)
        # return True

    def update(self, professor_id, name=None, email=None,
                        password=None):
        """Updates an existing Professor object and saves it to the repository."""
        return self.professor_service.update_professor(professor_id, name, email, password)
        # return True

    def remove(self, professor_id):
        """Removes an existing Professor object from the repository."""
        return self.professor_service.remove_professor(professor_id)
        # return True
