import re
import streamlit as st
from models import User
from utils import format_phone

def login_user(name: str, email: str, ddd: str, number: str) -> User:
    """Realiza o login ou registro de um novo usuário."""
    full_number = ddd.strip() + number.strip()
    formatted_phone = format_phone(full_number)

    # Verifica se o telefone está no formato correto
    if not re.fullmatch(r"\(\d{2}\) \d{4,5}-\d{4}", formatted_phone):
        raise ValueError("📞 Phone must be in format (99) 99999-9999 or (99) 9999-9999.")

    # Verifica se o usuário já existe
    existing_user = next((u for u in st.session_state.users if u.email == email), None)
    if existing_user:
        if existing_user.name == name:
            return existing_user  # Usuário já logado
        else:
            raise ValueError("❌ Email already exists with a different name.")
    else:
        # Novo usuário
        new_user = User(name=name.strip(), email=email.strip(), phone=formatted_phone)
        st.session_state.users.append(new_user)
        return new_user
