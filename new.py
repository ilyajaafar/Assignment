# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------
st.title("Lifestyle and Health Condition Dashboard 🩺")

# Load dataset directly from your GitHub repo
url = "https://raw.githubusercontent.com/ilyajaafar/Assignment/refs/heads/main/dataset.csv"

try:
    df = pd.read_csv(url)
    st.success("✅ Data successfully loaded from GitHub!")
    st.write(df.head())
except Exception as e:
    st.error("❌ Failed to load data. Please check your GitHub file link.")
    st.stop()

# -----------------------------------------------------------
# 1. Relationship between Smoking Habit and Health Conditions
# -----------------------------------------------------------
st.subheader("Relationship between Smoking Habit and Current Health Conditions")

smoking_health = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions'])
fig1 = px.bar(
    smoking_health,
    barmode='stack',
    title='Relationship between Smoking Habit and Current Health Conditions',
    labels={'index': 'Smoking Habit', 'value': 'Number of Respondents'}
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------------------------
# 2. Physical Activity vs Mental Health
# -----------------------------------------------------------
st.subheader("Relationship Between Physical Activity and Mental Health")

pivot = df.pivot_table(index='Physical Activity Level',
                       columns='Mental Health Frequency',
                       values='Age Group',
                       aggfunc='count',
                       fill_value=0).reset_index()

fig2 = px.imshow(
    pivot.set_index('Physical Activity Level'),
    text_auto=True,
    color_continuous_scale='YlGnBu',
    title="Physical Activity Level vs Mental Health Frequency"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------------
# 3. Mental Health Frequency by Smoking Habit
# -----------------------------------------------------------
st.subheader("Mental Health Frequency by Smoking Habit")

fig3 = px.histogram(
    df,
    x='Smoking Habit',
    color='Mental Health Frequency',
    barmode='group',
    title='Mental Health Frequency by Smoking Habit'
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------
# 4. Distribution of Symptoms by Diet Type
# -----------------------------------------------------------
st.subheader("Distribution of Symptoms by Diet Type")

symptom_diet = df.groupby(['Diet Type', 'symptoms']).size().unstack(fill_value=0)
fig4 = go.Figure()

for col in symptom_diet.columns:
    fig4.add_trace(go.Bar(
        x=symptom_diet.index,
        y=symptom_diet[col],
        name=col
    ))

fig4.update_layout(
    barmode='stack',
    title='Distribution of Symptoms by Diet Type',
    xaxis_title='Diet Type',
    yaxis_title='Count'
)
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------------
# 5. Smoking Habits by Gender (Pie Charts)
# -----------------------------------------------------------
st.subheader("Smoking Habits by Gender")

genders = df['Gender'].unique()
pie_cols = st.columns(len(genders))

for i, gender in enumerate(genders):
    data = df[df['Gender'] == gender]['Smoking H]()


