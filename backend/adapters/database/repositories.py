"""Database repositories module.

- Implementa as operações necessárias para o domínio salvar os dados
- Implementa a interface para salvar e recuperar dados do DB
- Aqui, pode ser usado qualquer tecnologia
"""

from sqlalchemy.orm import Session
from backend.core.domain.models import (
    Professor, Aluno
)
from backend.core.interfaces.repositories import(
    ProfessorRepository, AlunoRepository
    )


class ProfessorRepositoryPostgres(ProfessorRepository):
    """Professor repository class for PostgreSQL implementation."""

    def __init__(self, db: Session):
        """Initializes the repository with a database session."""
        self.db = db


    def verify_login(self, email: str, password: str) -> bool:
        """Verifies professor login credentials."""
        professor = self.db.query(Professor).filter(Professor.email == email).first()
        if professor is None:
            return False
        return professor.password == password

    def save(self, professor: Professor) -> Professor:
        """Saves a Professor object to the database."""
        self.db.add(professor)
        self.db.commit()
        self.db.refresh(professor)
        return professor

    def delete(self, professor: Professor) -> None:
        """Deletes a Professor object from the database."""
        self.db.delete(professor)
        self.db.commit()

    def get_by_id(self, professor_id: int) -> Professor:
        """Retrieves a Professor object from the database by its ID."""
        return self.db.query(Professor).filter(Professor.id == professor_id).first()



class AlunoRepositoryPostgres(AlunoRepository):
    """Aluno repository class for PostgreSQL implementation."""

    def __init__(self, db: Session):
        """Initializes the repository with a database session."""
        self.db = db


    def save(self, aluno: Aluno) -> Aluno:
        """Saves an Aluno object to the database."""
        self.db.add(aluno)
        self.db.commit()
        self.db.refresh(aluno)
        return aluno


    def get_by_id(self, aluno_id: int) -> Aluno:
        """Retrieves an Aluno object from the database by its ID."""
        return self.db.query(Aluno).filter(Aluno.id == aluno_id).first()


    def delete(self, aluno: Aluno) -> None:
        """Deletes an Aluno object from the database."""
        self.db.delete(aluno)
        self.db.commit()


    def get_by_name(self, aluno_name: str) -> list[Aluno]:
        """Retrieves one or more Aluno object from the database by its name.
        Args:
            aluno_name (str): Aluno name.
        Returns:
            list[Aluno]: List of Aluno objects.
        """
        return self.db.query(Aluno).filter(Aluno.name == aluno_name)
