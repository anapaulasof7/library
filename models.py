from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class User:
    """Representa um usuário da biblioteca."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    email: str = ""
    phone: str = ""

@dataclass
class Book:
    """Representa um livro na biblioteca."""
    title: str
    author: str
    publication_year: int
    available_copies: int
    total_copies: int
    is_borrowed: bool = False

@dataclass
class Loan:
    """Representa um empréstimo de um livro."""
    book: Book
    borrower: User
