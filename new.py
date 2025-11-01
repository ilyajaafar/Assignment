# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Lifestyle & Health Visualization Dashboard", layout="wide")
st.title("🩺 Lifestyle and Health Condition Dashboard")

# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------
url = "https://raw.githubusercontent.com/ilyajaafar/Assignment/main/dataset.csv"  # Change if needed

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(url)
    except Exception:
        st.warning("⚠️ Could not load from GitHub, please upload manually below.")
        uploaded = st.file_uploader("Upload your dataset (CSV)", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.stop()
    return df

df = load_data()
st.success("✅ Dataset successfully loaded!")
st.write("**Preview of dataset:**")
st.dataframe(df.head())

# -----------------------------------------------------------
# NAVIGATION
# -----------------------------------------------------------
page = st.sidebar.radio(
    "📊 Choose a Dashboard Section:",
    ["Lifestyle & Health Conditions", "Lifestyle by Age & Gender", "Access to Wellness by Region"]
)

# -----------------------------------------------------------
# PAGE 1: Lifestyle & Health Conditions
# -----------------------------------------------------------
if page == "Lifestyle & Health Conditions":
    st.header("🎯 Relationship between Lifestyle Habits and Health Conditions")

    col1, col2, col3 = st.columns(3)

    # 1. Smoking Habit vs Health Conditions
    with col1:
        if 'Smoking Habit' in df.columns and 'Current Health Conditions' in df.columns:
            cross = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions'])
            fig1 = px.bar(
                cross,
                barmode="stack",
                title="Smoking Habit vs Current Health Conditions",
                labels={'index': 'Smoking Habit', 'value': 'Count'}
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Required columns missing: 'Smoking Habit', 'Current Health Conditions'")

    # 2. Physical Activity vs Mental Health (Heatmap)
    with col2:
        if 'Physical Activity Level' in df.columns and 'Mental Health Frequency' in df.columns:
            pivot = df.pivot_table(
                index='Physical Activity Level',
                columns='Mental Health Frequency',
                values=df.columns[0],
                aggfunc='count',
                fill_value=0
            )
            fig2 = px.imshow(
                pivot,
                color_continuous_scale='YlGnBu',
                text_auto=True,
                title="Physical Activity Level vs Mental Health Frequency"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Required columns missing for heatmap.")

    # 3. Sleep Duration vs Physical Activity (Scatter)
    with col3:
        if 'Sleep Duration' in df.columns and 'Physical Activity Level' in df.columns:
            fig3 = px.scatter(
                df,
                x='Sleep Duration',
                y='Physical Activity Level',
                color='Mental Health Frequency' if 'Mental Health Frequency' in df.columns else None,
                title="Sleep Duration vs Physical Activity Level",
                labels={'Sleep Duration': 'Sleep (hours)', 'Physical Activity Level': 'Activity Level'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Columns 'Sleep Duration' or 'Physical Activity Level' missing.")

# -----------------------------------------------------------
# PAGE 2: Lifestyle by Age & Gender
# -----------------------------------------------------------
elif page == "Lifestyle by Age & Gender":
    st.header("🧍‍♀️ Lifestyle Behaviors Across Age Groups and Genders")

    col1, col2, col3 = st.columns(3)

    # 1. Average Sleep Duration by Age Group (Line)
    with col1:
        if 'Age Group' in df.columns and 'Sleep Duration' in df.columns:
            avg_sleep = df.groupby('Age Group')['Sleep Duration'].mean().reset_index()
            fig4 = px.line(
                avg_sleep,
                x='Age Group',
                y='Sleep Duration',
                markers=True,
                title="Average Sleep Duration by Age Group"
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Missing columns for sleep vs age group.")

    # 2. Smoking Habits by Gender (Pie)
    with col2:
        if 'Gender' in df.columns and 'Smoking Habit' in df.columns:
            genders = df['Gender'].dropna().unique()
            tabs = st.tabs([str(g).title() for g in genders])

            for i, gender in enumerate(genders):
                data = df[df['Gender'] == gender]['Smoking Habit'].value_counts().reset_index()
                data.columns = ['Smoking Habit', 'Count']
                with tabs[i]:
                    fig5 = px.pie(
                        data,
                        names='Smoking Habit',
                        values='Count',
                        hole=0.4,
                        title=f"Smoking Habits among {gender.title()}"
                    )
                    st.plotly_chart(fig5, use_container_width=True)
        else:
            st.warning("Required columns missing: 'Gender' or 'Smoking Habit'")

    # 3. BMI vs Age Group (Scatter)
    with col3:
        if 'BMI' in df.columns and 'Age Group' in df.columns:
            fig6 = px.box(
                df,
                x='Age Group',
                y='BMI',
                color='Gender' if 'Gender' in df.columns else None,
                title="BMI Distribution Across Age Groups"
            )
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.warning("Columns 'BMI' or 'Age Group' missing.")

# -----------------------------------------------------------
# PAGE 3: Access to Wellness by Region
# -----------------------------------------------------------
elif page == "Access to Wellness by Region":
    st.header("🌍 Access to Healthcare and Wellness Resources by Region")

    col1, col2, col3 = st.columns(3)

    # 1. Clean Water Access by Region
    with col1:
        if 'Region/Locality' in df.columns and 'Access to Clean Water & Sanitation' in df.columns:
            fig7 = px.histogram(
                df,
                y='Region/Locality',
                color='Access to Clean Water & Sanitation',
                title='Clean Water Access by Region',
                orientation='h'
            )
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.warning("Missing columns for clean water access plot.")

    # 2. Healthcare Visits vs Region (if available)
    with col2:
        if 'Region/Locality' in df.columns and 'Healthcare Visits' in df.columns:
            visits = df.groupby('Region/Locality')['Healthcare Visits'].mean().reset_index()
            fig8 = px.bar(
                visits,
                x='Region/Locality',
                y='Healthcare Visits',
                title='Average Healthcare Visits by Region'
            )
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("No 'Healthcare Visits' data available.")

    # 3. Wellness Program Participation (if available)
    with col3:
        if 'Wellness Program Participation' in df.columns:
            fig9 = px.pie(
                df,
                names='Wellness Program Participation',
                title="Participation in Wellness Programs"
            )
            st.plotly_chart(fig9, use_container_width=True)
        else:
            st.info("No 'Wellness Program Participation' column found.")

st.markdown("---")
st.caption("Data source: Mendeley Data | Visualization built using Streamlit & Plotly Express")




