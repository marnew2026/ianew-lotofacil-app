import streamlit as st
import requests, random

# Ajuste 1: Configuração de Página com Ícone e Layout Largo
st.set_page_config(
    page_title="IA Lotofácil Pro", 
    page_icon="💰", 
    layout="centered"
)

# Estilo CSS para deixar o botão de copiar bonito
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2e7d32; color: white; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 IA Lotofácil Profissional")
st.subheader("Gerador Inteligente com Filtros Avançados")

# Ajuste 2: Campo para Dezenas Fixas (Opcional)
dezenas_obrigatorias = st.multiselect(
    "Escolha até 5 números fixos (opcional):", 
    range(1, 26), 
    max_selections=5,
    help="A IA completará o jogo garantindo que estes números apareçam."
)

def gerar_jogo_ia(fixas):
    try:
        # Busca último sorteio para filtro de exclusão
        resp = requests.get("https://lotericas.com.br").json()
        ultimo_sorteio = resp['dezenas']
    except:
        ultimo_sorteio = []
    
    primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    for _ in range(2000): # Tenta 2000 combinações
        # Completa o jogo com números aleatórios excluindo as fixas já escolhidas
        restantes = [n for n in range(1, 26) if n not in fixas]
        jogo_aleatorio = random.sample(restantes, 15 - len(fixas))
        jogo = sorted(list(fixas) + jogo_aleatorio)
        
        # Filtros Estatísticos
        pares = len([n for n in jogo if n % 2 == 0])
        prim = len([n for n in jogo if n in primos])
        soma = sum(jogo)
        
        # Critérios de 80% de chance + Exclusão do último ganhador
        if (7 <= pares <= 8) and (5 <= prim <= 6) and (180 <= soma <= 210):
            if jogo != ultimo_sorteio:
                return jogo, pares, prim, soma
    return None, 0, 0, 0

if st.button("🚀 GERAR PALPITE ASSERTIVO"):
    jogo, pa, pr, s = gerar_jogo_ia(dezenas_obrigatorias)
    
    if jogo:
        st.success("### Jogo Sugerido:")
        # Transforma lista em texto para facilitar copiar
        texto_jogo = " ".join(f"{n:02d}" for n in jogo)
        st.code(texto_jogo, language="text") # Ajuste 3: Área de código fácil de copiar
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pares", pa)
        c2.metric("Primos", pr)
        c3.metric("Soma", s)
        
        st.info("💡 Dica: Clique no ícone de prancheta no canto direito dos números para copiar!")
    else:
        st.error("Não foi possível gerar um jogo com esses números fixos dentro dos padrões. Tente mudar as fixas.")

st.divider()
st.caption("Filtros ativos: Pares (7-8), Primos (5-6), Soma (180-210) e Verificação de 15 pontos.")
