import streamlit as st
from storage import initialize_storage, add_book, populate_default_books
from models import Book
from auth import login_user
from utils import loan_book, return_book
from report import generate_report_chart
import re

# ----------------------------
# CONFIGURAÇÃO DO STREAMLIT
# ----------------------------
st.set_page_config(page_title="Online Library")

# Inicializa o armazenamento da sessão
initialize_storage()

def show_login_form() -> None:
    """Exibe o formulário de login ou registro."""
    st.markdown("<h2 style='text-align: center;'>📚 Online Library</h2>", unsafe_allow_html=True)
    st.subheader("🔐 Sign In")
    with st.form("login_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")

        col1, col2 = st.columns([1, 3])
        with col1:
            ddd = st.text_input("DDD", max_chars=2)
        with col2:
            number = st.text_input("Phone Number", max_chars=9, help="Ex: 999999999")

        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                if not name.strip() or not email.strip() or not ddd.strip() or not number.strip():
                    st.error("⚠️ Please fill in all fields (Name, Email, DDD, and Phone Number).")
                elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                    st.error("⚠️ Invalid email format.")
                elif not ddd.isdigit():
                    st.error("⚠️ DDD must contain only numbers.")
                elif not number.isdigit():
                    st.error("⚠️ Phone Number must contain only numbers.")
                else:
                    user = login_user(name, email, ddd, number)
                    st.session_state.logged_user = user
                    st.success(f"✅ Logged in as {user.name.capitalize()}")
                    st.rerun()
            except ValueError as e:
                st.error(str(e))
def show_books() -> None:
    """Exibe os livros disponíveis e permite empréstimos e devoluções."""
    user = st.session_state.logged_user

    col_left, col_right = st.columns([2, 1.5])

    with col_left:
        header_col1, header_col2 = st.columns([5, 2])
        with header_col1:
            st.markdown("### 👤 User Information")
        with header_col2:
         if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_user = None
                st.rerun()

        st.success(f"✅ Logged in as: {user.name} ({user.email})")
        st.markdown(f"""
        📞 **Phone**: {user.phone}<br>
        🆔 **ID**: {user.id}
        """, unsafe_allow_html=True)

    with col_right:
        # Título e botão lado a lado
        header_col1, header_col2 = st.columns([7, 5])
        with header_col1:
            st.subheader("📚 Books")
        with header_col2:
            if len(st.session_state.users) > 0:
                buf = generate_report_chart()
                st.download_button(
                    label="📥 Report",
                    data=buf,
                    file_name="library_report.png",
                    mime="image/png",
                    use_container_width=True
                )

        if st.button("➕ Register a Book"):
            st.session_state.show_book_modal = True

        if not st.session_state.show_book_modal:
            search_query = st.text_input("Search by Title, Author or Year")
            filtered_books = [
            book for book in reversed(st.session_state.books)
            if search_query.lower() in book.title.lower() or
            search_query.lower() in book.author.lower() or
            str(book.publication_year).startswith(search_query)
            ]
        else:
            filtered_books = []

        if st.session_state.show_book_modal:
            with st.expander("📖 Add a New Book", expanded=True):
                title = st.text_input("Title", key="modal_title")
                author = st.text_input("Author", key="modal_author")
                publication_year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
                total_copies = st.number_input("Total Copies", min_value=1, step=1)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✅ Register"):
                        if title.strip() and author.strip():
                            book = Book(title.strip(), author.strip(), publication_year, total_copies, total_copies)
                            add_book(book)
                            st.success(f"Book '{title}' added.")
                            st.session_state.show_book_modal = False
                            st.rerun()
                        else:
                            st.warning("Please fill in all fields.")
                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.show_book_modal = False
                        st.rerun()

        if filtered_books:
            for b in filtered_books:
                book_status = (
                    "Available"
                    if not b.is_borrowed
                    else f"Borrowed by {next(loan.borrower.name for loan in st.session_state.loans if loan.book == b)}"
                )

                st.markdown(f"### {b.title} by {b.author}")
                st.write(f"Published: {b.publication_year}")
                st.write(f"Status: {book_status}")
                st.write(f"Available Copies: {b.available_copies}/{b.total_copies}")

                if not b.is_borrowed and b.available_copies > 0:
                    if st.button(f"Borrow {b.title}", key=f"borrow_{b.title}"):
                        if loan_book(b, user):
                            st.success(f"You have borrowed '{b.title}'.")
                            st.rerun()
                        else:
                            st.error(f"Unable to borrow '{b.title}'.")
                else:
                    if st.button(f"Return {b.title}", key=f"return_{b.title}"):
                        if return_book(b, user):
                            st.success(f"You have returned '{b.title}'.")
                            st.rerun()
                        else:
                            st.error(f"Unable to return '{b.title}'.")
        else:
            st.info("No books found for your search.")

# ----------------------------
# LÓGICA PRINCIPAL
# ----------------------------
if not st.session_state.logged_user:
    show_login_form()
else:
    populate_default_books()
    show_books()
