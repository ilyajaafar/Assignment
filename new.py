import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Lifestyle & Health Dashboard")

st.title("Lifestyle and Health Condition Dashboard 🩺")

# -------------------------
# Load dataset from GitHub
# -------------------------
url_try = "https://raw.githubusercontent.com/ilyajaafar/Assignment/refs/heads/main/dataset.csv"
url_fallback = "https://raw.githubusercontent.com/ilyajaafar/Assignment/main/dataset.csv"

def load_csv(urls):
    last_err = None
    for u in urls:
        try:
            df_local = pd.read_csv(u)
            return df_local
        except Exception as e:
            last_err = e
    raise last_err

try:
    df = load_csv([url_try, url_fallback])
    st.success("✅ Data successfully loaded from GitHub!")
    st.write(df.head())
except Exception as e:
    st.error("❌ Failed to load data. Please check your GitHub file link or upload a CSV.")
    uploaded_file = st.file_uploader("Or upload your CSV file manually", type="csv")
    if uploaded_file is None:
        st.stop()
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data loaded from uploaded file.")
    st.write(df.head())

# -----------------------------------------------------------
# 1. Relationship between Smoking Habit and Health Conditions
# -----------------------------------------------------------
st.subheader("Relationship between Smoking Habit and Current Health Conditions")

if 'Smoking Habit' in df.columns and 'Current Health Conditions' in df.columns:
    smoking_health = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions'])
    fig1 = px.bar(
        smoking_health,
        barmode='stack',
        title='Relationship between Smoking Habit and Current Health Conditions',
        labels={'index': 'Smoking Habit', 'value': 'Number of Respondents'}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Missing columns: 'Smoking Habit' or 'Current Health Conditions'")

# -----------------------------------------------------------
# 2. Physical Activity vs Mental Health
# -----------------------------------------------------------
st.subheader("Relationship Between Physical Activity and Mental Health")

if 'Physical Activity Level' in df.columns and 'Mental Health Frequency' in df.columns:
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
else:
    st.warning("Missing columns: 'Physical Activity Level' or 'Mental Health Frequency'")

# -----------------------------------------------------------
# 3. Mental Health Frequency by Smoking Habit
# -----------------------------------------------------------
st.subheader("Mental Health Frequency by Smoking Habit")

if 'Smoking Habit' in df.columns and 'Mental Health Frequency' in df.columns:
    fig3 = px.histogram(
        df,
        x='Smoking Habit',
        color='Mental Health Frequency',
        barmode='group',
        title='Mental Health Frequency by Smoking Habit'
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Missing columns: 'Smoking Habit' or 'Mental Health Frequency'")

# -----------------------------------------------------------
# 4. Distribution of Symptoms by Diet Type
# -----------------------------------------------------------
st.subheader("Distribution of Symptoms by Diet Type")

if 'Diet Type' in df.columns and 'symptoms' in df.columns:
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
else:
    st.warning("Missing columns: 'Diet Type' or 'symptoms'")

# -----------------------------------------------------------
# 5. Smoking Habits by Gender (Fixed)
# -----------------------------------------------------------
st.subheader("Smoking Habits by Gender")

if 'Gender' in df.columns and 'Smoking Habit' in df.columns:
    try:
        genders = df['Gender'].dropna().unique().tolist()

        if not genders:
            st.warning("No gender data found in the dataset.")
        else:
            cols = st.columns(len(genders))

            for i, gender_value in enumerate(genders):
                subset_df = df[df['Gender'] == gender_value]
                counts = subset_df['Smoking Habit'].value_counts().reset_index()
                counts.columns = ['Smoking Habit', 'Count']

                if not counts.empty:
                    fig = px.pie(
                        counts,
                        names='Smoking Habit',
                        values='Count',
                        title=f"Smoking Habits among {str(gender_value).title()}",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    cols[i].plotly_chart(fig, use_container_width=True)
                else:
                    cols[i].info(f"No smoking data for {gender_value}")

    except Exception as e:
        st.error(f"Error displaying pie charts: {e}")
else:
    st.warning("Missing columns: 'Gender' or 'Smoking Habit'")

# -----------------------------------------------------------
# 6. Clean Water Access by Region
# -----------------------------------------------------------
st.subheader("Clean Water Access by Region")

if 'Region/Locality' in df.columns and 'Access to Clean Water & Sanitation' in df.columns:
    fig6 = px.histogram(
        df,
        y='Region/Locality',
        color='Access to Clean Water & Sanitation',
        title='Clean Water Access by Region',
        orientation='h'
    )
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("Missing columns: 'Region/Locality' or 'Access to Clean Water & Sanitation'")




