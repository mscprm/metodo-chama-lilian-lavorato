import streamlit as st
import pandas as pd

# ----------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Diário de Bordo C.H.A.M.A.",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS CSS CUSTOMIZADOS (PALETA OFICIAL DO MÉTODO)
st.markdown("""
<style>
    .stApp {
        background-color: #FDFBF7;
    }
    .header-box {
        background-color: #1A3644;
        color: white;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #FFFFFF;
        margin-top: 10px;
        margin-bottom: 4px;
    }
    .header-subtitle {
        font-size: 15px;
        color: #E2E8F0;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .header-collab {
        font-size: 14px;
        font-weight: 700;
        color: #F4A261;
        letter-spacing: 0.8px;
    }
    .avatar-img-header {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid #F4A261;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }
    .avatar-img-card {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        border: 2px solid #1A3644;
    }
    .dicas-ouro-card {
        background-color: #FEF9E7;
        border-left: 6px solid #F4A261;
        padding: 16px 20px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
    }
    .chama-badge {
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .cuidometro-box {
        background-color: #11242E;
        color: #A8E6CF;
        padding: 16px;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        border: 2px solid #2E8B57;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# GERENCIAMENTO DE ESTADO (SESSION STATE)
# ----------------------------------------------------
if 'cuidometro' not in st.session_state:
    st.session_state['cuidometro'] = 25

if 'acordo_fechado' not in st.session_state:
    st.session_state['acordo_fechado'] = False

if 'cliente_selecionado' not in st.session_state:
    st.session_state['cliente_selecionado'] = "Distribuidora Alfa Ltda."

if 'perfil_ativo' not in st.session_state:
    st.session_state['perfil_ativo'] = "Carla (A Apertada)"

# ----------------------------------------------------
# BARRA LATERAL (LINHA DO TEMPO C.H.A.M.A. & TREINAMENTO)
# ----------------------------------------------------
with st.sidebar:
    st.image("data:image/png;base64,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", width=90)
    st.title("Linha do Tempo C.H.A.M.A.")
    st.caption("Guia Pedagógico de Apoio ao Treinamento")
    
    fase_treino = st.radio(
        "Consulta de Etapas (Apoio ao Operador):",
        [
            "C · Conhecer (Prevenção & Análise)",
            "H · Humanizar (WhatsApp & Abordagem)",
            "A · Agir no Tempo Certo (Régua de Cobrança)",
            "M · Mediar (Negociação & Alçadas)",
            "A · Acompanhar (Ritual da Parcela & Redoma)"
        ],
        index=3
    )
    
    st.markdown("---")
    if "Conhecer" in fase_treino:
        st.info("**C · Conhecer**: Mapeie a carteira e confirme a baixa bancária antes de qualquer contato. Prevenção é a primeira linha da cobrança.")
    elif "Humanizar" in fase_treino:
        st.info("**H · Humanizar**: Personalize a mensagem com nome, fato sem julgamento e facilidade (PIX). Respeite horários e a linguagem do cliente.")
    elif "Agir" in fase_treino:
        st.info("**A · Agir no Tempo Certo**: Cumpra os prazos da régua. Lembre-se do Art. 42 do CDC: nunca expor ou constranger o cliente.")
    elif "Mediar" in fase_treino:
        st.info("**M · Mediar**: Escute o motivo do atraso. Use a Calculadora de Alçadas para negociar com autonomia sem perder a margem.")
    else:
        st.info("**A · Acompanhar**: Fechou o acordo? Mova o cliente para a Redoma de Proteção e acompanhe as parcelas no D-2.")

# ----------------------------------------------------
# CABEÇALHO PRINCIPAL (BIA CENTRALIZADA)
# ----------------------------------------------------
st.markdown("""
<div class="header-box">
    <img src="data:image/png;base64,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" class="avatar-img-header"><br>
    <div class="header-title">DIÁRIO DE BORDO DIGITAL · MÉTODO C.H.A.M.A.</div>
    <div class="header-subtitle">Autoria Intelectual: Lilian Lavorato (A Arte da Cobrança Humanizada)</div>
    <div class="header-collab">Collab MGP - Métodos, Gestão e Projetos</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# RÉGUA C.H.A.M.A. & CUIDÔMETRO
# ----------------------------------------------------
col_regua, col_cuido = st.columns([3.5, 1.2])

with col_regua:
    st.subheader("Régua de Operação C.H.A.M.A.")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    st_acordo = st.session_state['acordo_fechado']
    
    lbl_c = "✓ CONCLUÍDO" if st_acordo else "✓ OK"
    lbl_h = "✓ CONCLUÍDO" if st_acordo else "✓ OK"
    lbl_a1 = "✓ CONCLUÍDO" if st_acordo else "⏳ EM ANDAMENTO"
    lbl_m = "✓ CONCLUÍDO" if st_acordo else "PENDENTE"
    lbl_a2 = "✓ REDOMA ATIVA" if st_acordo else "PENDENTE"
    
    bg_m = "#A8E6CF" if st_acordo else "#D0E1E9"
    bg_a2 = "#A8E6CF" if st_acordo else "#D0E1E9"

    c1.markdown(f'<div class="chama-badge" style="background-color: #A8E6CF; color: #11242E;">C · Conhecer<br>{lbl_c}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="chama-badge" style="background-color: #FFD3B6; color: #11242E;">H · Humanizar<br>{lbl_h}</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="chama-badge" style="background-color: #FFAAA5; color: #11242E;">A · Agir<br>{lbl_a1}</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="chama-badge" style="background-color: {bg_m}; color: #11242E;">M · Mediar<br>{lbl_m}</div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="chama-badge" style="background-color: {bg_a2}; color: #11242E;">A · Acompanhar<br>{lbl_a2}</div>', unsafe_allow_html=True)

with col_cuido:
    val_cuido = st.session_state['cuidometro']
    st.markdown(f"""
    <div class="cuidometro-box">
        💚 CUIDÔMETRO<br>
        <span style="font-size: 26px;">{val_cuido}</span><br>
        <span style="font-size: 12px; font-weight: normal; color: #E2E8F0;">Relações Preservadas no Mês</span>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# QUADRO DE DICAS DE OURO DA LILIAN (AUTORA DO MÉTODO)
# ----------------------------------------------------
st.markdown("""
<div class="dicas-ouro-card">
    <div style="font-size: 16px; font-weight: bold; color: #1A3644; margin-bottom: 6px;">
        💡 Dicas de Ouro da Lilian Lavorato (Apoio ao Operador em Treinamento)
    </div>
    <div style="font-size: 14px; color: #2C3E50; line-height: 1.5;">
        • <b>Cobrar é Cuidar:</b> <i>"Cobrar não é confrontar. É oferecer uma solução e cuidar de uma relação que vale a pena manter."</i><br>
        • <b>Regra da Negociação:</b> <i>"Troque concessão por compromisso! Nunca conceda desconto sem pedir a garantia da entrada em até 24h."</i><br>
        • <b>Pausar é Técnica:</b> <i>"Se a conversa esquentar, diga: 'Entendo que o momento é difícil. Prefere que eu te ligue amanhã às 10h para seguirmos com calma?'"</i>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------
# PAINEL DE EMPATIA (AVATARES ILUSTRADOS)
# ----------------------------------------------------
st.subheader("Painel de Empatia (Perfis Comportamentais do Livro)")
st.caption("Clique no avatar do perfil ou selecione na carteira abaixo para adaptar a estratégia:")

col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)

with col_a1:
    st.markdown('<div style="text-align:center;"><img src="data:image/png;base64,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" class="avatar-img-card"></div>', unsafe_allow_html=True)
    if st.button("👓 Seu Jorge", key="btn_jorge", use_container_width=True):
        st.session_state['perfil_ativo'] = "Seu Jorge (O Esquecido)"
        st.session_state['cliente_selecionado'] = "Mercearia do Jorge Ltda."

with col_a2:
    st.markdown('<div style="text-align:center;"><img src="data:image/png;base64,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" class="avatar-img-card"></div>', unsafe_allow_html=True)
    if st.button("👩🏾 Carla", key="btn_carla", use_container_width=True):
        st.session_state['perfil_ativo'] = "Carla (A Apertada)"
        st.session_state['cliente_selecionado'] = "Distribuidora Alfa Ltda."

with col_a3:
    st.markdown('<div style="text-align:center;"><img src="data:image/png;base64,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" class="avatar-img-card"></div>', unsafe_allow_html=True)
    if st.button("👨🏼 Rafael", key="btn_rafael", use_container_width=True):
        st.session_state['perfil_ativo'] = "Rafael (O Contestador)"
        st.session_state['cliente_selecionado'] = "Tech Logística S.A."

with col_a4:
    st.markdown('<div style="text-align:center;"><img src="data:image/png;base64,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" class="avatar-img-card"></div>', unsafe_allow_html=True)
    if st.button("👵🏼 Dona Marta", key="btn_marta", use_container_width=True):
        st.session_state['perfil_ativo'] = "Dona Marta (A Sumida)"
        st.session_state['cliente_selecionado'] = "Marta Confecções EIRELI"

with col_a5:
    st.markdown('<div style="text-align:center;"><img src="data:image/png;base64,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" class="avatar-img-card"></div>', unsafe_allow_html=True)
    if st.button("🧔🏻 Léo", key="btn_leo", use_container_width=True):
        st.session_state['perfil_ativo'] = "Léo (O Promitente)"
        st.session_state['cliente_selecionado'] = "Léo Eventos & Produções"

# EXIBIÇÃO DO PERFIL ATIVO
perf = st.session_state['perfil_ativo']
if "Seu Jorge" in perf:
    st.info("**Perfil Ativo: Seu Jorge (O Esquecido)** — *Tem o dinheiro, mas perdeu o boleto na correria.* **Estratégia:** Lembrete amigável com código PIX copia e cola.")
elif "Carla" in perf:
    st.info("**Perfil Ativo: Carla (A Apertada)** — *Quer pagar, mas o caixa não fecha agora.* **Estratégia:** Escuta ativa e Calculadora de Alçadas para parcelamento.")
elif "Rafael" in perf:
    st.info("**Perfil Ativo: Rafael (O Contestador)** — *Acha que a cobrança está errada.* **Estratégia:** Conferência prévia de notas e comprovantes antes de insistir.")
elif "Dona Marta" in perf:
    st.info("**Perfil Ativo: Dona Marta (A Sumida)** — *Visualiza e não responde por vergonha.* **Estratégia:** Mensagem curta em opções numeradas simples (1, 2, 3).")
else:
    st.info("**Perfil Ativo: Léo (O Promitente)** — *Promete uma data e a data passa.* **Estratégia:** Registro por escrito e contato no exato dia do compromisso.")

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------
# CARTEIRA DE CLIENTES SELECIONÁVEL
# ----------------------------------------------------
st.subheader("Carteira de Atendimento Interativa")
st.write("Selecione o cliente na lista para carregar os dados e a persona correspondente:")

clientes_dados = [
    {"Cliente": "Distribuidora Alfa Ltda.", "Valor (R$)": "5.000,00", "Atraso": "18 dias", "Perfil": "Carla (A Apertada)", "Status": "Aguardando Proposta"},
    {"Cliente": "Mercearia do Jorge Ltda.", "Valor (R$)": "1.200,00", "Atraso": "2 dias", "Perfil": "Seu Jorge (O Esquecido)", "Status": "Enviar PIX"},
    {"Cliente": "Tech Logística S.A.", "Valor (R$)": "8.500,00", "Atraso": "12 dias", "Perfil": "Rafael (O Contestador)", "Status": "Conferir NF"},
    {"Cliente": "Marta Confecções EIRELI", "Valor (R$)": "3.400,00", "Atraso": "25 dias", "Perfil": "Dona Marta (A Sumida)", "Status": "Menu 1, 2, 3"},
    {"Cliente": "Léo Eventos & Produções", "Valor (R$)": "4.100,00", "Atraso": "7 dias", "Perfil": "Léo (O Promitente)", "Status": "Confirmar Data"}
]

cli_nomes = [c["Cliente"] for c in clientes_dados]
index_sel = cli_nomes.index(st.session_state['cliente_selecionado']) if st.session_state['cliente_selecionado'] in cli_nomes else 0

cliente_escolhido = st.selectbox("Selecione o Cliente em Atendimento:", cli_nomes, index=index_sel)

if cliente_escolhido != st.session_state['cliente_selecionado']:
    st.session_state['cliente_selecionado'] = cliente_escolhido
    for c in clientes_dados:
        if c["Cliente"] == cliente_escolhido:
            st.session_state['perfil_ativo'] = c["Perfil"]
            st.rerun()

df_cli = pd.DataFrame(clientes_dados)
st.dataframe(df_cli, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# TRILHA HORIZONTAL DO CHECKLIST DE SEGURANÇA (INTERATIVO)
# ----------------------------------------------------
st.subheader("Trilha de Segurança Obrigatória Pré-Contato (Checklist do Operador)")
st.caption("Marque cada item verificado para garantir a conformidade antes da abordagem:")

ck1, ck2, ck3, ck4, ck5 = st.columns(5)

val_ck1 = ck1.checkbox("1. Baixa no ERP?", value=True, help="Conferiu se o pagamento entrou nos últimos 30 min?")
val_ck2 = ck2.checkbox("2. Art. 42 CDC?", value=True, help="Garantir que não haverá exposição ou constrangimento.")
val_ck3 = ck3.checkbox("3. Confirmou Titular?", value=True, help="Só tratar de valores diretamente com o responsável.")
val_ck4 = ck4.checkbox("4. Tom Não-Violento?", value=False, help="Abordagem focada em solução e acolhimento.")
val_ck5 = ck5.checkbox("5. Leu Histórico?", value=False, help="Analisou negociações anteriores e promessas.")

tudo_ok = val_ck1 and val_ck2 and val_ck3 and val_ck4 and val_ck5
if tudo_ok:
    st.success("✅ **Trilha de Segurança 100% Verificada!** Operador liberado para efetuar o contato com total conformidade.")
else:
    st.warning("⚠️ **Trilha de Segurança Pendente:** Marque todos os itens acima para garantir o contato seguro.")

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------
# CALCULADORA INTELIGENTE DE ALÇADAS & GAVETA DA BIA
# ----------------------------------------------------
col_calc, col_gaveta = st.columns([1, 1.1])

with col_calc:
    st.subheader("Calculadora Inteligente de Alçadas")
    st.write(f"**Simulação de Proposta para: {st.session_state['cliente_selecionado']}**")
    
    ent = st.number_input("Valor da Entrada (R$):", value=1000.0, step=100.0)
    parc = st.slider("Número de Parcelas:", 1, 6, 4)
    desc = st.checkbox("Isenção de Juros/Multa (100%)", value=True)
    
    if parc <= 3 and ent >= 1000.0:
        st.success("🟢 **Farol Verde (Nível Analista):** Proposta aprovada automaticamente na sua alçada!")
    elif parc <= 5:
        st.warning("🟡 **Farol Amarelo (Nível Coordenação):** Exige validação do coordenador. *💡 A Bia lembra: Troque concessão por compromisso!*")
    else:
        st.error("🔴 **Farol Vermelho (Nível Diretoria):** Proposta acima da alçada padrão. Requer parecer do comitê.")

with col_gaveta:
    st.subheader("Gaveta da Bia (Modelo WhatsApp)")
    st.write(f"**Mensagem Adaptada para {perf}:**")
    
    if "Carla" in perf:
        msg_txt = "Olá Carla, tudo bem? Aqui é a Bia. Entendemos o momento da Distribuidora Alfa. Conseguimos organizar uma entrada de R$ 1.000,00 e 4 parcelas fixas sem juros. Podemos formalizar para manter seu crédito protegido?"
    elif "Seu Jorge" in perf:
        msg_txt = "Oi, Seu Jorge, bom dia! Aqui é a Bia. O boleto de R$ 1.200,00 venceu ontem. Segue o PIX copia e cola para facilitar: [00020126...]. Se já pagou, me envia o comprovante que dou baixa!"
    elif "Rafael" in perf:
        msg_txt = "Olá Rafael! Tudo bem? Aqui é a Bia. Conforme solicitado, estou reenviando a Nota Fiscal e o comprovante de entrega da Tech Logística. Podemos confirmar o pagamento para hoje?"
    elif "Dona Marta" in perf:
        msg_txt = "Olá Dona Marta! Aqui é a Bia. Para facilitar a regularização da Marta Confecções, escolha uma das opções: 1- Pagar via PIX à vista | 2- Parcelar em 3x | 3- Ligar para conversarmos."
    else:
        msg_txt = "Olá Léo! Tudo bem? Passando para confirmar nosso compromisso agendado para hoje referente ao título da Léo Eventos. Segue a chave PIX para quitação."
        
    st.text_area("Texto Formatado Pronto para Envio:", value=msg_txt, height=120)
    
    if st.button("🤝 Confirmar Acordo & Mover para Redoma", use_container_width=True):
        st.session_state['cuidometro'] += 1
        st.session_state['acordo_fechado'] = True
        st.balloons()
        st.success(f"🎉 **Acordo Confirmado com Sucesso!** O cliente {st.session_state['cliente_selecionado']} foi movido para a **Redoma do Acordo Ativo** e o Cuidômetro subiu para **{st.session_state['cuidometro']} relações preservadas**!")
        st.rerun()

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Apoio Pedagógico ao Treinamento A Arte da Cobrança Humanizada (Lilian Lavorato) · Collab MGP - Métodos, Gestão e Projetos")
