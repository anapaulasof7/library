import re

def format_phone(phone: str) -> str:
    """Formata o número de telefone para o padrão (99) 99999-9999."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return phone

def loan_book(book, user):
    """Realiza o empréstimo de um livro."""
    if not book.is_borrowed and book.available_copies > 0:
        book.is_borrowed = True
        book.available_copies -= 1
        return True
    return False

def return_book(book, user):
    """Realiza a devolução de um livro."""
    if book.is_borrowed:
        book.is_borrowed = False
        book.available_copies += 1
        return True
    return False
