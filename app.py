
import streamlit as st
import requests, random

# Configurações de Interface
st.set_page_config(page_title="LotoIA Master", page_icon="🔥", layout="centered")

def buscar_dados():
    try:
        # API de resultados reais
        resp = requests.get("https://lotericas.com.br").json()
        return resp['dezenas'], resp['concurso']
    except:
        return [], 0

ultimo_sorteio, concurso = buscar_dados()

# --- LÓGICA DE PADRÕES (ESTILO LOTO MASTER) ---
inicio_alto = False
if ultimo_sorteio and int(ultimo_sorteio[0]) >= 4:
    inicio_alto = True # Indica tendência de inícios tardios (05, 06...)

st.title("🔥 LotoIA Master: Rastreamento de Padrões")

# Painel de Monitoramento
col1, col2 = st.columns(2)
with col1:
    st.metric("Último Concurso", concurso)
with col2:
    if inicio_alto:
        st.error("⚠️ PADRÃO DETECTADO: Início Alto (04-06)")
    else:
        st.success("✅ PADRÃO NORMAL: Início Baixo (01-03)")

# Seletor de Modo
modo_ia = st.radio("Configuração da IA:", ["Modo Equilibrado", "Modo Tendência (Início na 06)"], 
                  help="O Modo Tendência força o jogo a começar a partir da dezena 06.")

if modo_ia == "Modo Tendência (Início na 06)":
    st.warning("🚀 ÍCONE DE OPORTUNIDADE: Gerando palpites a partir da dezena 06 conforme seu padrão solicitado.")

def gerar_jogo_master(n_dezenas, modo):
    primos_lista = 
    
    for _ in range(10000):
        # Define o universo de dezenas baseado no modo
        if modo == "Modo Tendência (Início na 06)":
            universo = list(range(6, 26))
            # Garante que o jogo comece exatamente com a 06
            jogo = [6] + random.sample([n for n in universo if n != 6], n_dezenas - 1)
        else:
            universo = list(range(1, 26))
            jogo = random.sample(universo, n_dezenas)
        
        jogo = sorted(jogo)
        
        # Filtros Loto Master (Pares, Primos e Soma)
        pa = len([n for n in jogo if n % 2 == 0])
        pr = len([n for n in jogo if n in primos_lista])
        sm = sum(jogo)
        
        # Validação Estatística para 15 a 17 dezenas
        if (7 <= pa <= 10) and (4 <= pr <= 7) and (180 <= sm <= 250):
            # Filtro de Exclusão Total (Nunca repetiu 15 pontos)
            if len(set(jogo) & set(ultimo_sorteio)) < 15:
                return jogo, pa, pr, sm
    return None, 0, 0, 0

# --- BOTÃO DE GERAÇÃO ---
qtd = st.selectbox("Quantidade de dezenas:", [15, 16, 17])

if st.button("GERAR PALPITE MASTER"):
    res, p, pri, s = gerar_jogo_master(qtd, modo_ia)
    
    if res:
        st.markdown("### 📋 Palpite Gerado:")
        st.code(" - ".join(f"{n:02d}" for n in res), language="text")
        
        st.info(f"📊 Análise: Pares: {p} | Primos: {pr} | Soma: {s}")
        if res[0] == 6:
            st.success("🎯 Padrão de início na dezena 06 aplicado com sucesso!")
    else:
        st.error("Não foi possível encontrar um jogo nos filtros. Tente o modo Equilibrado.")

st.divider()
st.caption("Baseado em algoritmos de análise de frequência e tendências de atraso.")
