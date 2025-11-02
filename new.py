import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Load the dataset
# -----------------------------
df = pd.read_csv("dataset (1).csv")

st.title("Objective 1: Relationship Between Lifestyle Habits and Health Conditions")

# -----------------------------
# Visualization 1: Smoking Habit vs Health Conditions (Clustered Bar)
# -----------------------------
st.subheader("1️⃣ Relationship between Smoking Habit and Current Health Conditions")

smoking_health_crosstab = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions']).reset_index()
smoking_melted = smoking_health_crosstab.melt(id_vars='Smoking Habit', var_name='Health Condition', value_name='Count')

fig1 = px.bar(
    smoking_melted,
    x='Smoking Habit',
    y='Count',
    color='Health Condition',
    barmode='group',
    title='Relationship between Smoking Habit and Current Health Conditions'
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Visualization 2: Fast Food Consumption Frequency (Pie Chart)
# -----------------------------
st.subheader("2️⃣ Distribution of Fast Food Consumption Frequency")

fastfood_counts = df['Fast Food Consumption Frequency'].value_counts().reset_index()
fastfood_counts.columns = ['Fast Food Consumption Frequency', 'Count']

fig2 = px.pie(
    fastfood_counts,
    values='Count',
    names='Fast Food Consumption Frequency',
    title='Distribution of Fast Food Consumption Frequency',
    hole=0.3
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Visualization 3: Current Health Conditions (Pie Chart)
# -----------------------------
st.subheader("3️⃣ Distribution of Current Health Conditions")

health_conditions_counts = df['Current Health Conditions'].value_counts().reset_index()
health_conditions_counts.columns = ['Current Health Conditions', 'Count']

fig3 = px.pie(
    health_conditions_counts,
    values='Count',
    names='Current Health Conditions',
    title='Distribution of Current Health Conditions',
    hole=0.3
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Visualization 4: Physical Activity vs Mental Health (Heatmap)
# -----------------------------
st.subheader("4️⃣ Relationship Between Physical Activity and Mental Health")

pivot = df.pivot_table(
    index='Physical Activity Level',
    columns='Mental Health Frequency',
    values='Age Group',
    aggfunc='count',
    fill_value=0
)

fig4 = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='YlGnBu'
    )
)

fig4.update_layout(
    title='Relationship Between Physical Activity and Mental Health',
    xaxis_title='Mental Health Frequency',
    yaxis_title='Physical Activity Level'
)
st.plotly_chart(fig4, use_container_width=True)
# ==============================================================
# OBJECTIVE 2: Compare Lifestyle Behaviors Across Different Age Groups and Genders
# ==============================================================

st.header("🎯 Objective 2: Compare Lifestyle Behaviors Across Different Age Groups and Genders")

# -----------------------------
# Visualization 1: Physical Activity Level by Gender
# -----------------------------
st.subheader("1️⃣ Physical Activity Level by Gender")

fig1 = px.histogram(
    df,
    x='Physical Activity Level',
    color='Gender',
    barmode='group',
    title='Physical Activity Level by Gender'
)
fig1.update_layout(
    xaxis_title='Physical Activity Level',
    yaxis_title='Count',
    xaxis_tickangle=45
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Visualization 2: Smoking Habits by Gender (Pie Charts Side-by-Side)
# -----------------------------
st.subheader("2️⃣ Smoking Habits by Gender")

# Group and count
gender_smoke = df.groupby('Gender')['Smoking Habit'].value_counts().unstack(fill_value=0)

# Create one pie chart per gender
pie_charts = []
for gender in gender_smoke.index:
    gender_data = gender_smoke.loc[gender]
    fig = px.pie(
        values=gender_data.values,
        names=gender_data.index,
        title=f"Smoking Habits among {gender}s",
        hole=0.3
    )
    pie_charts.append(fig)

# Display side-by-side
cols = st.columns(len(pie_charts))
for i, col in enumerate(cols):
    with col:
        st.plotly_chart(pie_charts[i], use_container_width=True)

# -----------------------------
# Visualization 3: Fast Food Consumption Frequency by Age Group
# -----------------------------
st.subheader("3️⃣ Fast Food Consumption Frequency by Age Group")

fastfood_age_crosstab = pd.crosstab(df['Age Group'], df['Fast Food Consumption Frequency']).reset_index()
fastfood_melted = fastfood_age_crosstab.melt(id_vars='Age Group', var_name='Fast Food Frequency', value_name='Count')

fig3 = px.line(
    fastfood_melted,
    x='Age Group',
    y='Count',
    color='Fast Food Frequency',
    markers=True,
    title='Fast Food Consumption Frequency by Age Group'
)
fig3.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Number of Respondents',
    legend_title='Fast Food Consumption Frequency'
)
st.plotly_chart(fig3, use_container_width=True)
# ==============================================================
# OBJECTIVE 3: Visualize Access to Healthcare and Wellness Resources By Region
# ==============================================================

st.header("🎯 Objective 3: Visualize Access to Healthcare and Wellness Resources by Region")

# -----------------------------
# Visualization 1: Access to Clean Water & Sanitation by Region/Locality
# -----------------------------
st.subheader("1️⃣ Access to Clean Water & Sanitation by Region/Locality")

water_access_region_crosstab = pd.crosstab(df['Region/Locality'], df['Access to Clean Water & Sanitation']).reset_index()
water_access_melted = water_access_region_crosstab.melt(id_vars='Region/Locality', var_name='Access Type', value_name='Count')

fig1 = px.bar(
    water_access_melted,
    x='Region/Locality',
    y='Count',
    color='Access Type',
    barmode='stack',
    title='Access to Clean Water & Sanitation by Region/Locality'
)
fig1.update_layout(
    xaxis_title='Region/Locality',
    yaxis_title='Number of Respondents',
    xaxis_tickangle=45
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Visualization 2: Healthcare Access Method by Region/Locality
# -----------------------------
st.subheader("2️⃣ Healthcare Access Method by Region/Locality")

healthcare_access_region_pivot = df.pivot_table(
    index='Region/Locality',
    columns='Healthcare Access Method',
    values='Name',  # Any column just for counting
    aggfunc='count',
    fill_value=0
).reset_index()

# Melt for heatmap style
healthcare_melted = healthcare_access_region_pivot.melt(id_vars='Region/Locality', var_name='Healthcare Method', value_name='Count')

fig2 = px.density_heatmap(
    healthcare_melted,
    x='Healthcare Method',
    y='Region/Locality',
    z='Count',
    color_continuous_scale='YlGnBu',
    title='Healthcare Access Method by Region/Locality'
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Visualization 3: Mental Health Frequency by Region/Locality
# -----------------------------
st.subheader("3️⃣ Mental Health Frequency by Region/Locality")

mental_health_region_crosstab = pd.crosstab(df['Region/Locality'], df['Mental Health Frequency']).reset_index()
mental_health_melted = mental_health_region_crosstab.melt(id_vars='Region/Locality', var_name='Mental Health Frequency', value_name='Count')

fig3 = px.line(
    mental_health_melted,
    x='Region/Locality',
    y='Count',
    color='Mental Health Frequency',
    markers=True,
    title='Mental Health Frequency by Region/Locality'
)
fig3.update_layout(
    xaxis_title='Region/Locality',
    yaxis_title='Number of Respondents',
    legend_title='Mental Health Frequency',
    xaxis_tickangle=45
)
st.plotly_chart(fig3, use_container_width=True)






