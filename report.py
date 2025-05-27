import matplotlib.pyplot as plt
import io
import streamlit as st

def generate_report_chart():
    """Gera um gráfico de resumo da biblioteca."""
    
    # Dados simulados (substitua com os dados reais de st.session_state)
    livros_disponiveis = sum(b.available_copies for b in st.session_state.books)
    livros_emprestados = sum(b.total_copies - b.available_copies for b in st.session_state.books)
    usuarios_cadastrados = len(st.session_state.users)  # Pega os usuários do storage

    # Criando o gráfico
    fig, ax = plt.subplots()
    bars = ax.bar(
        ["Available", "Borrowed", "Users"],
        [livros_disponiveis, livros_emprestados, usuarios_cadastrados],
        color=["green", "orange", "blue"]
    )
    ax.set_title("Library Overview", fontsize=10)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adicionando os números acima das barras manualmente
    ax.text(bars[0].get_x() + bars[0].get_width() / 2, bars[0].get_height() + 0.1, 
            f'{bars[0].get_height()}', ha='center', va='bottom', fontsize=10)
    
    ax.text(bars[1].get_x() + bars[1].get_width() / 2, bars[1].get_height() + 0.1, 
            f'{bars[1].get_height()}', ha='center', va='bottom', fontsize=10)
    
    ax.text(bars[2].get_x() + bars[2].get_width() / 2, bars[2].get_height() + 0.1, 
            f'{bars[2].get_height()}', ha='center', va='bottom', fontsize=10)

    # Salvando o gráfico em um buffer de memória
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)  # Retorna ao início do buffer
    return buf
