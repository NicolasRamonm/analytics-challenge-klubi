import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Análise de Hábitos e Desempenho Estudantil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Análise Interativa de Hábitos e Desempenho Estudantil")
st.markdown("---")

# Carregamento dos dados
@st.cache_data
def load_data():
    """Carrega os dados do CSV"""
    try:
        df = pd.read_csv('data/habitos_e_desempenho_estudantil.csv')
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Certifique-se de que o arquivo está na pasta 'data/'")
        return None

# Carregar dados
df = load_data()

if df is not None:
    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por gênero
    gender_options = ['Todos'] + list(df['gender'].unique())
    selected_gender = st.sidebar.selectbox("Gênero", gender_options)
    
    # Filtro por faixa etária
    age_min, age_max = st.sidebar.slider(
        "Faixa etária", 
        int(df['age'].min()), 
        int(df['age'].max()), 
        (int(df['age'].min()), int(df['age'].max()))
    )
    
    # Filtro por qualidade da dieta
    diet_options = ['Todos'] + list(df['diet_quality'].unique())
    selected_diet = st.sidebar.selectbox("Qualidade da Dieta", diet_options)
    
    # Filtro por educação parental
    education_options = ['Todos'] + [x for x in df['parental_education_level'].unique() if pd.notna(x)]
    selected_education = st.sidebar.selectbox("Educação Parental", education_options)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_gender != 'Todos':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    
    filtered_df = filtered_df[
        (filtered_df['age'] >= age_min) & 
        (filtered_df['age'] <= age_max)
    ]
    
    if selected_diet != 'Todos':
        filtered_df = filtered_df[filtered_df['diet_quality'] == selected_diet]
    
    if selected_education != 'Todos':
        filtered_df = filtered_df[filtered_df['parental_education_level'] == selected_education]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Estudantes", len(filtered_df))
    
    with col2:
        avg_score = filtered_df['exam_score'].mean()
        st.metric("Nota Média", f"{avg_score:.1f}")
    
    with col3:
        avg_study_hours = filtered_df['study_hours_per_day'].mean()
        st.metric("Horas de Estudo/Dia", f"{avg_study_hours:.1f}")
    
    with col4:
        avg_attendance = filtered_df['attendance_percentage'].mean()
        st.metric("Frequência Média", f"{avg_attendance:.1f}%")
    
    st.markdown("---")
    
    # Tabs para diferentes análises
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Desempenho vs Hábitos", 
        "👥 Análise Demográfica", 
        "💤 Estilo de Vida", 
        "📊 Correlações", 
        "🎯 Insights"
    ])
    
    with tab1:
        st.header("📈 Relação entre Desempenho e Hábitos de Estudo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot: Horas de estudo vs Nota
            fig1 = px.scatter(
                filtered_df, 
                x='study_hours_per_day', 
                y='exam_score',
                color='gender',
                size='attendance_percentage',
                hover_data=['age', 'diet_quality', 'sleep_hours'],
                title="Horas de Estudo vs Nota no Exame",
                labels={'study_hours_per_day': 'Horas de Estudo por Dia', 'exam_score': 'Nota no Exame'}
            )
            fig1.update_layout(height=500)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Box plot: Notas por gênero
            fig2 = px.box(
                filtered_df, 
                x='gender', 
                y='exam_score',
                title="Distribuição de Notas por Gênero",
                labels={'gender': 'Gênero', 'exam_score': 'Nota no Exame'}
            )
            fig2.update_layout(height=500)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfico de barras: Média de notas por qualidade da dieta
        fig3 = px.bar(
            filtered_df.groupby('diet_quality')['exam_score'].mean().reset_index(),
            x='diet_quality',
            y='exam_score',
            title="Nota Média por Qualidade da Dieta",
            labels={'diet_quality': 'Qualidade da Dieta', 'exam_score': 'Nota Média'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.header("👥 Análise Demográfica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por gênero
            gender_counts = filtered_df['gender'].value_counts()
            fig1 = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Distribuição por Gênero"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Distribuição por idade
            fig2 = px.histogram(
                filtered_df, 
                x='age',
                nbins=20,
                title="Distribuição por Idade",
                labels={'age': 'Idade', 'count': 'Frequência'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Educação parental vs desempenho
        fig3 = px.box(
            filtered_df, 
            x='parental_education_level', 
            y='exam_score',
            title="Desempenho por Nível de Educação Parental",
            labels={'parental_education_level': 'Educação Parental', 'exam_score': 'Nota no Exame'}
        )
        fig3.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.header("💤 Análise de Estilo de Vida")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Horas de sono vs desempenho
            fig1 = px.scatter(
                filtered_df, 
                x='sleep_hours', 
                y='exam_score',
                color='diet_quality',
                title="Horas de Sono vs Desempenho",
                labels={'sleep_hours': 'Horas de Sono', 'exam_score': 'Nota no Exame'}
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Frequência de exercício vs desempenho
            fig2 = px.box(
                filtered_df, 
                x='exercise_frequency', 
                y='exam_score',
                title="Frequência de Exercício vs Desempenho",
                labels={'exercise_frequency': 'Frequência de Exercício', 'exam_score': 'Nota no Exame'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Mídias sociais e entretenimento
        fig3 = px.scatter(
            filtered_df, 
            x='social_media_hours', 
            y='netflix_hours',
            size='exam_score',
            color='gender',
            title="Uso de Mídias Sociais vs Netflix (tamanho = nota)",
            labels={'social_media_hours': 'Horas de Mídias Sociais', 'netflix_hours': 'Horas de Netflix'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        st.header("📊 Análise de Correlações")
        
        # Matriz de correlação
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        correlation_matrix = filtered_df[numeric_cols].corr()
        
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Matriz de Correlação",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlações com exam_score
        exam_correlations = correlation_matrix['exam_score'].abs().sort_values(ascending=False)
        exam_correlations = exam_correlations.drop('exam_score')  # Remove self-correlation
        
        fig2 = px.bar(
            x=exam_correlations.values,
            y=exam_correlations.index,
            orientation='h',
            title="Correlações com Nota no Exame",
            labels={'x': 'Correlação Absoluta', 'y': 'Variável'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab5:
        st.header("🎯 Insights e Recomendações")
        
        # Análise de grupos de desempenho
        filtered_df['performance_group'] = pd.cut(
            filtered_df['exam_score'], 
            bins=[0, 50, 70, 85, 100], 
            labels=['Baixo', 'Médio', 'Bom', 'Excelente']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Características dos estudantes de alto desempenho
            high_performers = filtered_df[filtered_df['performance_group'] == 'Excelente']
            
            st.subheader("🏆 Características dos Estudantes de Alto Desempenho")
            
            if len(high_performers) > 0:
                st.write(f"**Total:** {len(high_performers)} estudantes")
                st.write(f"**Horas médias de estudo:** {high_performers['study_hours_per_day'].mean():.1f}")
                st.write(f"**Frequência média:** {high_performers['attendance_percentage'].mean():.1f}%")
                st.write(f"**Horas médias de sono:** {high_performers['sleep_hours'].mean():.1f}")
                
                # Qualidade da dieta dos melhores
                diet_dist = high_performers['diet_quality'].value_counts()
                st.write("**Distribuição por qualidade da dieta:**")
                for diet, count in diet_dist.items():
                    st.write(f"- {diet}: {count} ({count/len(high_performers)*100:.1f}%)")
            else:
                st.write("Nenhum estudante com desempenho excelente encontrado com os filtros aplicados.")
        
        with col2:
            # Recomendações baseadas nos dados
            st.subheader("💡 Recomendações")
            
            # Calcular médias para recomendações
            avg_study = filtered_df['study_hours_per_day'].mean()
            avg_sleep = filtered_df['sleep_hours'].mean()
            avg_attendance = filtered_df['attendance_percentage'].mean()
            
            st.write("**Baseado na análise dos dados:**")
            
            if avg_study < 4:
                st.write("📚 **Estudo:** Aumentar horas de estudo (média atual: {:.1f}h/dia)".format(avg_study))
            
            if avg_sleep < 7:
                st.write("😴 **Sono:** Melhorar qualidade do sono (média atual: {:.1f}h)".format(avg_sleep))
            
            if avg_attendance < 85:
                st.write("📅 **Frequência:** Melhorar assiduidade (média atual: {:.1f}%)".format(avg_attendance))
            
            # Análise de correlação para recomendações
            study_corr = filtered_df['study_hours_per_day'].corr(filtered_df['exam_score'])
            sleep_corr = filtered_df['sleep_hours'].corr(filtered_df['exam_score'])
            attendance_corr = filtered_df['attendance_percentage'].corr(filtered_df['exam_score'])
            
            st.write("**Correlações mais fortes com desempenho:**")
            correlations = [
                ("Horas de Estudo", study_corr),
                ("Horas de Sono", sleep_corr),
                ("Frequência", attendance_corr)
            ]
            
            for name, corr in sorted(correlations, key=lambda x: abs(x[1]), reverse=True):
                direction = "positiva" if corr > 0 else "negativa"
                st.write(f"• {name}: {corr:.3f} (correlação {direction})")
    
    # Footer
    st.markdown("---")
    st.markdown("**Dados:** Análise de hábitos e desempenho estudantil | **Ferramenta:** Streamlit + Plotly")

else:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo 'habitos_e_desempenho_estudantil.csv' está na pasta 'data/'")
