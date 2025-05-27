import streamlit as st
from models import User, Book, Loan

def initialize_storage():
    """Verifica se os dados necessários estão na sessão do Streamlit."""
    if "users" not in st.session_state:
        st.session_state.users = []

    if "books" not in st.session_state:
        st.session_state.books = []

    if "loans" not in st.session_state:
        st.session_state.loans = []

    if "logged_user" not in st.session_state:
        st.session_state.logged_user = None

    if "show_book_modal" not in st.session_state:
        st.session_state.show_book_modal = False

def populate_default_books() -> None:
    """Popula a biblioteca com livros padrão se a lista de livros estiver vazia."""
    if not st.session_state.books:
        st.session_state.books = [
            Book(title="1984", author="George Orwell", publication_year=1949, available_copies=3, total_copies=5),
            Book(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960, available_copies=2, total_copies=4),
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", publication_year=1925, available_copies=4, total_copies=6),
            Book(title="Pride and Prejudice", author="Jane Austen", publication_year=1813, available_copies=5, total_copies=5),
            Book(title="One Hundred Years of Solitude", author="Gabriel García Márquez", publication_year=1967, available_copies=3, total_copies=5)
        ]

def add_book(book: Book) -> None:
    """Adiciona um novo livro à biblioteca."""
    st.session_state.books.append(book)
