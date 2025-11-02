import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------------
# Load the dataset
# --------------------------------------------------------
df = pd.read_csv("dataset (1).csv")

# Map gender abbreviations to full words
df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female', 'm': 'Male', 'f': 'Female'})
st.set_page_config(page_title="Lifestyle & Health Dashboard", layout="wide")

st.title("🏥 Lifestyle & Health Data Visualization Dashboard")
st.markdown("Explore insights into **lifestyle habits**, **demographics**, and **wellness resources**.")

# --------------------------------------------------------
# Create tabs for each Objective
# --------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Objective 1: Lifestyle Habits vs Health Conditions",
    "🎯 Objective 2: Lifestyle Behaviors Across Age & Gender",
    "🎯 Objective 3: Healthcare & Wellness by Region"
])

# ========================================================
# 🟢 OBJECTIVE 1
# ========================================================
with tab1:
    st.header("Objective 1: Relationship Between Lifestyle Habits and Health Conditions")

    # 1️⃣ Smoking Habit vs Current Health Conditions
    st.subheader("1️⃣ Relationship between Smoking Habit and Current Health Conditions")
    smoking_health = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions']).reset_index()
    melted1 = smoking_health.melt(id_vars='Smoking Habit', var_name='Health Condition', value_name='Count')

    fig1 = px.bar(
        melted1, x='Smoking Habit', y='Count', color='Health Condition',
        barmode='stack', title='Smoking Habit vs Current Health Conditions'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Fast Food Consumption Frequency
    st.subheader("2️⃣ Distribution of Fast Food Consumption Frequency")
    fastfood_counts = df['Fast Food Consumption Frequency'].value_counts().reset_index()
    fastfood_counts.columns = ['Fast Food Consumption Frequency', 'Count']

    fig2 = px.pie(
        fastfood_counts, values='Count', names='Fast Food Consumption Frequency',
        title='Distribution of Fast Food Consumption Frequency', hole=0.3
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Current Health Conditions
    st.subheader("3️⃣ Distribution of Current Health Conditions")
    health_counts = df['Current Health Conditions'].value_counts().reset_index()
    health_counts.columns = ['Current Health Conditions', 'Count']

    fig3 = px.pie(
        health_counts, values='Count', names='Current Health Conditions',
        title='Distribution of Current Health Conditions', hole=0.3
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Physical Activity vs Mental Health (Bar instead of heatmap)
    st.subheader("4️⃣ Relationship Between Physical Activity and Mental Health Frequency")
    pivot = pd.crosstab(df['Physical Activity Level'], df['Mental Health Frequency']).reset_index()
    melted4 = pivot.melt(id_vars='Physical Activity Level', var_name='Mental Health Frequency', value_name='Count')

    fig4 = px.bar(
        melted4, x='Physical Activity Level', y='Count', color='Mental Health Frequency',
        barmode='group', title='Physical Activity vs Mental Health Frequency'
    )
    st.plotly_chart(fig4, use_container_width=True)


# ========================================================
# 🟣 OBJECTIVE 2
# ========================================================
with tab2:
    st.header("Objective 2: Compare Lifestyle Behaviors Across Different Age Groups and Genders")

    # 1️⃣ Physical Activity Level by Gender
    st.subheader("1️⃣ Physical Activity Level by Gender")
    fig5 = px.histogram(
        df, x='Physical Activity Level', color='Gender',
        barmode='group', title='Physical Activity Level by Gender'
    )
    fig5.update_layout(xaxis_title='Physical Activity Level', yaxis_title='Count', xaxis_tickangle=45)
    st.plotly_chart(fig5, use_container_width=True)

    # 2️⃣ Smoking Habits by Gender
    st.subheader("2️⃣ Smoking Habits by Gender")
    gender_smoke = df.groupby('Gender')['Smoking Habit'].value_counts().unstack(fill_value=0)

    cols = st.columns(len(gender_smoke.index))
    for i, gender in enumerate(gender_smoke.index):
        gender_data = gender_smoke.loc[gender]
        fig = px.pie(
            values=gender_data.values, names=gender_data.index,
            title=f"Smoking Habits among {gender}", hole=0.3
        )
        with cols[i]:
            st.plotly_chart(fig, use_container_width=True)

    # 3️⃣ Fast Food Consumption Frequency by Age Group
    st.subheader("3️⃣ Fast Food Consumption Frequency by Age Group")
    fastfood_age = pd.crosstab(df['Age Group'], df['Fast Food Consumption Frequency']).reset_index()
    melted6 = fastfood_age.melt(id_vars='Age Group', var_name='Fast Food Frequency', value_name='Count')

    fig6 = px.line(
        melted6, x='Age Group', y='Count', color='Fast Food Frequency', markers=True,
        title='Fast Food Consumption Frequency by Age Group'
    )
    fig6.update_layout(
        xaxis_title='Age Group', yaxis_title='Number of Respondents',
        legend_title='Fast Food Consumption Frequency'
    )
    st.plotly_chart(fig6, use_container_width=True)


# ========================================================
# 🟠 OBJECTIVE 3
# ========================================================
with tab3:
    st.header("Objective 3: Visualize Access to Healthcare and Wellness Resources by Region")

    # 1️⃣ Access to Clean Water & Sanitation by Region/Locality
    st.subheader("1️⃣ Access to Clean Water & Sanitation by Region/Locality")
    water_access = pd.crosstab(df['Region/Locality'], df['Access to Clean Water & Sanitation']).reset_index()
    melted7 = water_access.melt(id_vars='Region/Locality', var_name='Access Type', value_name='Count')

    fig7 = px.bar(
        melted7, x='Region/Locality', y='Count', color='Access Type', barmode='stack',
        title='Access to Clean Water & Sanitation by Region/Locality'
    )
    fig7.update_layout(xaxis_title='Region/Locality', yaxis_title='Number of Respondents', xaxis_tickangle=45)
    st.plotly_chart(fig7, use_container_width=True)

    # 2️⃣ Healthcare Access Method by Region/Locality (Bar instead of Heatmap)
    st.subheader("2️⃣ Healthcare Access Method by Region/Locality")
    healthcare = df.pivot_table(
        index='Region/Locality', columns='Healthcare Access Method',
        values='Name', aggfunc='count', fill_value=0
    ).reset_index()
    melted8 = healthcare.melt(id_vars='Region/Locality', var_name='Healthcare Method', value_name='Count')

    fig8 = px.bar(
        melted8, x='Region/Locality', y='Count', color='Healthcare Method',
        barmode='group', title='Healthcare Access Method by Region/Locality'
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 3️⃣ Mental Health Frequency by Region/Locality
    st.subheader("3️⃣ Mental Health Frequency by Region/Locality")
    mental_health = pd.crosstab(df['Region/Locality'], df['Mental Health Frequency']).reset_index()
    melted9 = mental_health.melt(id_vars='Region/Locality', var_name='Mental Health Frequency', value_name='Count')

    fig9 = px.line(
        melted9, x='Region/Locality', y='Count', color='Mental Health Frequency', markers=True,
        title='Mental Health Frequency by Region/Locality'
    )
    fig9.update_layout(
        xaxis_title='Region/Locality', yaxis_title='Number of Respondents',
        legend_title='Mental Health Frequency', xaxis_tickangle=45
    )
    st.plotly_chart(fig9, use_container_width=True)






