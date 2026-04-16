import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import io

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="CityBike AI ",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CHARGEMENT DONNÉES / MODÈLE
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv('train_clean.csv')

@st.cache_resource
def load_model():
    try:
        return joblib.load('modele_foret_velo.joblib')
    except:
        return None

df = load_data()
model = load_model()

# ==========================================
# 3. LE GRAND HACK CSS "DARK SAAS"
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0b0f19; }
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1f2937; }

    /* Cartes Dashboard */
    .saas-card {
        background-color: #1f2937; border: 1px solid #374151; border-radius: 12px;
        padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); margin-bottom: 24px;
        display: flex; flex-direction: column; transition: all 0.3s ease;
    }
    .saas-card:hover { transform: translateY(-3px); border-color: #3b82f6; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2); }
    .card-label { color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem; margin-bottom: 8px; }
    .card-value { color: #f9fafb; font-size: 2.2rem; font-weight: 800; margin-bottom: 12px; }
    .card-trend { font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 4px; }
    .trend-up { color: #10b981; } .trend-down { color: #ef4444; }

    /* Alerte Critique (Nouveau) */
    .alert-card {
        background-color: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; border-radius: 12px;
        padding: 20px; text-align: center; margin-top: 15px; box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #9ca3af; font-weight: 600; font-size: 1.1rem; border-bottom: 2px solid transparent; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom-color: #3b82f6 !important; }

    h1, h2, h3, h4, p, label { color: #e5e7eb !important; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. FONCTION MINI-GRAPHIQUES
# ==========================================
def generate_sparkline(dataframe, y_col, color='#3b82f6'):
    df_daily = dataframe.groupby(pd.to_datetime(dataframe['datetime']).dt.date)[y_col].sum().reset_index()
    fig = px.line(df_daily, x='datetime', y=y_col, color_discrete_sequence=[color])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0),
                      xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=False, visible=False),
                      showlegend=False, height=60)
    return fig

# ==========================================
# 5. SIDEBAR & HEADER
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #ffffff !important; font-weight: 800; font-size: 1.8rem; margin:0;'>CityBike AI</h1>
            <p style='color: #3b82f6 !important; font-weight: 600; font-size: 0.9rem;'>Dark SaaS Platform</p>
        </div><hr style='border-color: #374151;'>
    """, unsafe_allow_html=True)
    st.markdown("### 🔍 FILTRES (Dashboard)")
    selected_season = st.selectbox("Sélectionner une Saison", ["Toutes", "Printemps", "Été", "Automne", "Hiver"])
    df_filtered = df if selected_season == "Toutes" else df[df['season'] == selected_season]

st.markdown(f"""
    <div style='margin-bottom: 2rem; border-left: 4px solid #3b82f6; padding-left: 1rem;'>
        <h1 style='color: #f9fafb !important; font-weight: 800; font-size: 2.2rem; margin-bottom: 0;'>Centre de Commandement</h1>
        <p style='color: #9ca3af !important; font-size: 1.1rem; margin-top: 0.2rem;'>Saison active : <b style='color:#3b82f6'>{selected_season}</b></p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 6. ARCHITECTURE EN ONGLETS
# ==========================================
tab1, tab2 = st.tabs(["📊 DASHBOARD ANALYTIQUE", "🤖 SIMULATEUR IA & FORECAST"])

# ------------------------------------------
# ONGLET 1 : DASHBOARD (Identique à avant)
# ------------------------------------------
with tab1:
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f'<div class="saas-card"><div class="card-label">Volume Total</div><div class="card-value">{df_filtered["count"].sum():,}</div><div class="card-trend trend-up">↗ +12.4% vs N-1</div></div>', unsafe_allow_html=True)
        st.plotly_chart(generate_sparkline(df_filtered, 'count', '#10b981'), config={'displayModeBar': False}, use_container_width=True)
    with kpi_col2:
        st.markdown(f'<div class="saas-card"><div class="card-label">Temp. Ressentie Moy.</div><div class="card-value">{df_filtered["atemp"].mean():.1f} °C</div><div class="card-trend trend-down">↘ -3% vs Norme</div></div>', unsafe_allow_html=True)
        st.plotly_chart(generate_sparkline(df_filtered, 'atemp', '#f59e0b'), config={'displayModeBar': False}, use_container_width=True)
    with kpi_col3:
        st.markdown(f'<div class="saas-card"><div class="card-label">Demande Moy. au Pic</div><div class="card-value">{int(df_filtered.groupby("hour")["count"].mean().max())}</div><div class="card-trend trend-up">↗ Record</div></div>', unsafe_allow_html=True)
        st.plotly_chart(generate_sparkline(df_filtered, 'registered', '#3b82f6'), config={'displayModeBar': False}, use_container_width=True)

    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.markdown("<h4 style='color: #f9fafb;'>Charge horaire par usager</h4>", unsafe_allow_html=True)
        df_hour_melt = pd.melt(df_filtered.groupby('hour')[['registered', 'casual']].mean().reset_index(), id_vars=['hour'], var_name='Type_Client', value_name='Volume')
        fig_main1 = px.bar(df_hour_melt, x='hour', y='Volume', color='Type_Client', color_discrete_sequence=['#3b82f6', '#4b5563'])
        fig_main1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), legend=dict(orientation="h", y=1.02, x=1, font=dict(color='#9ca3af')), hovermode="x unified", font=dict(color='#9ca3af'))
        fig_main1.update_xaxes(showgrid=False, linecolor='#374151', title=""); fig_main1.update_yaxes(gridcolor='#1f2937', title="")
        st.plotly_chart(fig_main1, config={'displayModeBar': False}, use_container_width=True)
    with col_chart2:
        st.markdown("<h4 style='color: #f9fafb;'>Répartition</h4>", unsafe_allow_html=True)
        fig_donut = px.pie(pd.DataFrame({'Client': ['Abonnés', 'Occasionnels'], 'Volume': df_filtered[['registered', 'casual']].sum().values}), values='Volume', names='Client', hole=0.7, color_discrete_sequence=['#3b82f6', '#1f2937'])
        fig_donut.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color='#0b0f19', width=2)))
        fig_donut.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), height=350, showlegend=True, legend=dict(orientation="h", y=-0.1, x=0.5, font=dict(color='#9ca3af')))
        st.plotly_chart(fig_donut, config={'displayModeBar': False}, use_container_width=True)

    st.markdown("<hr style='border-color: #1f2937; margin: 2rem 0;'>", unsafe_allow_html=True)
    if model is not None and hasattr(model, 'feature_importances_'):
        st.markdown("<h4 style='color: #f9fafb;'>🧠 Transparence IA : Moteurs de la demande (Top 10)</h4>", unsafe_allow_html=True)
        df_imp = pd.DataFrame({'Variable': model.feature_names_in_, 'Importance': model.feature_importances_}).sort_values(by='Importance').tail(10)
        df_imp['Variable'] = df_imp['Variable'].str.replace('_', ' : ').str.title()
        fig_imp = px.bar(df_imp, x='Importance', y='Variable', orientation='h', color_discrete_sequence=['#10b981'])
        fig_imp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), height=350, font=dict(color='#9ca3af'))
        fig_imp.update_xaxes(showgrid=True, gridcolor='#1f2937', title="Poids dans la décision"); fig_imp.update_yaxes(showgrid=False, title="")
        st.plotly_chart(fig_imp, config={'displayModeBar': False}, use_container_width=True)

# ------------------------------------------
# ONGLET 2 : SIMULATEUR IA + FORECAST 24H + ALERTES + EXPORT
# ------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_res = st.columns([1, 2.5], gap="large")

    with col_input:
        with st.form("ml_form_dark"):
            st.markdown("<h3 style='color: #f9fafb;'>🎛️ Paramètres</h3>", unsafe_allow_html=True)
            s_year = st.selectbox("Année", [2011, 2012], index=1)
            s_month = st.slider("Mois", 1, 12, 6)
            s_hour = st.slider("Heure de la journée", 0, 23, 8)
            s_atemp = st.slider("Température ressentie (°C)", -10.0, 50.0, 22.0)
            s_hum = st.slider("Humidité (%)", 0, 100, 50)
            s_season = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_type = st.radio("Type de Jour", ["jour semaine ouvrable", "week-end/jour férié"])
            s_holiday = st.checkbox("Jour Férié officiel")
            
            submitted = st.form_submit_button("LANCER L'INFÉRENCE IA", use_container_width=True)

    with col_res:
        if submitted:
            if model:
                try:
                    features = model.feature_names_in_
                    
                    # --- ÉTAPE 1 : Prédiction pour l'heure H précise ---
                    input_df = pd.DataFrame(0.0, index=[0], columns=features)
                    for col in ['year', 'month', 'hour', 'atemp', 'humidity']:
                        if col in features: input_df.at[0, col] = float(locals()[f"s_{'year' if col=='year' else 'month' if col=='month' else 'hour' if col=='hour' else 'atemp' if col=='atemp' else 'hum'}"])
                    if f"season_{s_season}" in features: input_df.at[0, f"season_{s_season}"] = 1.0
                    if f"workingday_{s_type}" in features: input_df.at[0, f"workingday_{s_type}"] = 1.0
                    h_str = "jour férié" if s_holiday else "jour non férié"
                    if f"holiday_{h_str}" in features: input_df.at[0, f"holiday_{h_str}"] = 1.0

                    pred = model.predict(input_df)[0]
                    
                    # --- NOUVEAUTÉ : ALERTE LOGISTIQUE SI > 350 ---
                    st.markdown("<h3 style='color: #f9fafb;'>🎯 Focus sur l'heure choisie</h3>", unsafe_allow_html=True)
                    col_focus1, col_focus2 = st.columns([1, 1])
                    
                    with col_focus1:
                        st.markdown(f"""
                            <div style="background-color: #1e3a8a; border: 2px solid #3b82f6; border-radius: 12px; padding: 30px; text-align: center;">
                                <p style="color: #93c5fd; font-weight: 600; text-transform: uppercase;">Demande Estimée ({s_hour}h00)</p>
                                <h1 style="color: #ffffff; font-size: 4rem; margin: 0;">{int(pred)} 🚲</h1>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_focus2:
                        if pred > 350:
                            st.markdown(f"""
                                <div class="alert-card">
                                    <h3 style="color: #ef4444; margin:0;">⚠️ ALERTE RUPTURE</h3>
                                    <p style="color: #fca5a5; font-size: 1.1rem;">La demande projetée dépasse la capacité moyenne des stations. Déploiement des camions de rééquilibrage recommandé d'urgence.</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div style="background-color: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; border-radius: 12px; padding: 20px; text-align: center; margin-top: 15px;">
                                    <h3 style="color: #10b981; margin:0;">✅ FLUX NOMINAL</h3>
                                    <p style="color: #6ee7b7;">Volume gérable par la rotation naturelle. Aucune intervention logistique lourde requise.</p>
                                </div>
                            """, unsafe_allow_html=True)

                    # --- NOUVEAUTÉ : FORECAST SUR 24 HEURES ---
                    st.markdown("<hr style='border-color: #1f2937;'>", unsafe_allow_html=True)
                    st.markdown("<h3 style='color: #f9fafb;'>📈 Forecast sur 24 Heures</h3>", unsafe_allow_html=True)
                    
                    # On génère un tableau pour les 24h en gardant la même météo/saison
                    forecast_data = []
                    for h in range(24):
                        row = input_df.copy()
                        if 'hour' in features:
                            row['hour'] = float(h)
                        forecast_data.append(row)
                    
                    forecast_df = pd.concat(forecast_data, ignore_index=True)
                    preds_24h = model.predict(forecast_df)
                    
                    # Dataframe pour le graphique
                    plot_df = pd.DataFrame({'Heure': range(24), 'Demande Estimee': preds_24h})
                    
                    # Graphique stylisé de prévision
                    fig_forecast = px.area(plot_df, x='Heure', y='Demande Estimee', color_discrete_sequence=['#8b5cf6']) # Violet Néon
                    fig_forecast.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=10, b=10, l=10, r=10), height=300, font=dict(color='#9ca3af'),
                        hovermode="x unified"
                    )
                    fig_forecast.update_xaxes(showgrid=False, linecolor='#374151', tickmode='linear', dtick=2)
                    fig_forecast.update_yaxes(gridcolor='#1f2937')
                    
                    # On ajoute une ligne pointillée rouge pour montrer le seuil critique (350)
                    fig_forecast.add_hline(y=350, line_dash="dot", line_color="#ef4444", annotation_text="Seuil Critique", annotation_position="top left", annotation_font_color="#ef4444")
                    
                    st.plotly_chart(fig_forecast, config={'displayModeBar': False}, use_container_width=True)

                    # --- NOUVEAUTÉ : BOUTON D'EXPORT CSV ---
                    st.markdown("<br>", unsafe_allow_html=True)
                    csv = plot_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Exporter le Forecast 24h (CSV)",
                        data=csv,
                        file_name=f"forecast_velos_m{s_month}_{s_type}.csv",
                        mime="text/csv",
                    )
                    
                except Exception as e:
                    st.error(f"Erreur de pipeline : {e}")
        else:
            st.markdown("""
                <div style="background-color: #1f2937; border: 1px dashed #4b5563; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
                    <p style="color: #9ca3af; font-size: 1.1rem;">En attente de paramètres...<br>L'IA générera un Forecast complet sur 24h.</p>
                </div>
            """, unsafe_allow_html=True)