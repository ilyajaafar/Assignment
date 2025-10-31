# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Lifestyle & Health Dashboard")

st.title("Lifestyle and Health Condition Dashboard 🩺")

# -------------------------
# Load dataset from GitHub
# -------------------------
# Original URL you provided (may not always be a raw link)
url_try = "https://raw.githubusercontent.com/ilyajaafar/Assignment/refs/heads/main/dataset.csv"
# Common working raw URL pattern fallback
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
    st.write("Preview (first 5 rows):")
    st.dataframe(df.head())
except Exception as e:
    st.error("❌ Failed to load data from GitHub. Please check the file link or upload a CSV below.")
    st.exception(e)
    uploaded_file = st.file_uploader("Or upload your CSV file", type="csv")
    if uploaded_file is None:
        st.stop()
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data loaded from uploaded file")
    st.dataframe(df.head())

# -------------------------
# Helper: check column
# -------------------------
def has_cols(*cols):
    missing = [c for c in cols if c not in df.columns]
    return len(missing) == 0, missing

st.markdown("---")

# Sidebar simple navigation
page = st.sidebar.radio("Choose view", [
    "All charts",
    "Smoking vs Health",
    "Activity vs Mental Health",
    "Symptoms by Diet",
    "Smoking by Gender",
    "Clean Water by Region"
])

# Layout: use container and columns for nicer look
container = st.container()

# -------------------------
# 1. Relationship between Smoking Habit and Current Health Conditions
# -------------------------
def smoking_vs_health():
    ok, missing = has_cols('Smoking Habit', 'Current Health Conditions')
    if not ok:
        st.warning(f"Missing columns for this chart: {missing}")
        return
    st.subheader("Relationship between Smoking Habit and Current Health Conditions")
    smoking_health = pd.crosstab(df['Smoking Habit'], df['Current Health Conditions'])
    # convert to long format for plotly express
    smoking_health_long = smoking_health.reset_index().melt(id_vars='Smoking Habit', var_name='Current Health Conditions', value_name='count')
    fig1 = px.bar(smoking_health_long,
                  x='Smoking Habit',
                  y='count',
                  color='Current Health Conditions',
                  title='Relationship between Smoking Habit and Current Health Conditions',
                  labels={'count': 'Number of Respondents'})
    st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# 2. Physical Activity vs Mental Health
# -------------------------
def activity_vs_mental():
    ok, missing = has_cols('Physical Activity Level', 'Mental Health Frequency')
    if not ok:
        st.warning(f"Missing columns for this chart: {missing}")
        return
    st.subheader("Relationship Between Physical Activity and Mental Health")
    pivot = df.pivot_table(index='Physical Activity Level',
                           columns='Mental Health Frequency',
                           values=df.columns[0],  # use any column for count
                           aggfunc='count',
                           fill_value=0)
    # ensure the pivot index/columns are sorted for consistent display
    pivot = pivot.sort_index().reindex(sorted(pivot.columns), axis=1)
    fig2 = px.imshow(pivot,
                     text_auto=True,
                     color_continuous_scale='YlGnBu',
                     aspect="auto",
                     title="Physical Activity Level vs Mental Health Frequency",
                     labels=dict(x="Mental Health Frequency", y="Physical Activity Level", color="Count"))
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# 3. Mental Health Frequency by Smoking Habit
# -------------------------
def mental_by_smoking():
    ok, missing = has_cols('Smoking Habit', 'Mental Health Frequency')
    if not ok:
        st.warning(f"Missing columns for this chart: {missing}")
        return
    st.subheader("Mental Health Frequency by Smoking Habit")
    fig3 = px.histogram(df,
                        x='Smoking Habit',
                        color='Mental Health Frequency',
                        barmode='group',
                        title='Mental Health Frequency by Smoking Habit',
                        labels={'count': 'Number of Respondents'})
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# 4. Distribution of Symptoms by Diet Type
# -------------------------
def symptoms_by_diet():
    ok, missing = has_cols('Diet Type', 'symptoms')
    if not ok:
        st.warning(f"Missing columns for this chart: {missing}")
        return
    st.subheader("Distribution of Symptoms by Diet Type")
    symptom_diet = df.groupby(['Diet Type', 'symptoms']).size().unstack(fill_value=0)
    fig4 = go.Figure()
    for col in symptom_diet.columns:
        fig4.add_trace(go.Bar(
            x=symptom_diet.index.astype(str),
            y=symptom_diet[col],
            name=str(col)
        ))
    fig4.update_layout(
        barmode='stack',
        title='Distribution of Symptoms by Diet Type',
        xaxis_title='Diet Type',
        yaxis_title='Count',
        legend_title='Symptoms'
    )
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------------
# 5. Smoking Habits by Gender (Pie Charts)
# -----------------------------------------------------------
st.subheader("Smoking Habits by Gender")

genders = df['Gender'].unique()
cols = st.columns(len(genders))

for i, gender in enumerate(genders):
    subset = df[df['Gender'] == gender]
    smoking_counts = subset['Smoking Habit'].value_counts().reset_index()
    smoking_counts.columns = ['Smoking Habit', 'Count']

    fig7 = px.pie(
        smoking_counts,
        names='Smoking Habit',
        values='Count',
        title=f"Smoking Habits among {gender}",
        hole=0.4
    )

    with cols[i]:
        st.plotly_chart(fig7, use_container_width=True)


# -------------------------
# Page router
# -------------------------
if page == "All charts":
    with container:
        smoking_vs_health()
        st.markdown("---")
        activity_vs_mental()
        st.markdown("---")
        mental_by_smoking()
        st.markdown("---")
        symptoms_by_diet()
        st.markdown("---")
        smoking_by_gender()
        st.markdown("---")
        water_by_region()
else:
    with container:
        if page == "Smoking vs Health":
            smoking_vs_health()
        elif page == "Activity vs Mental Health":
            activity_vs_mental()
        elif page == "Symptoms by Diet":
            symptoms_by_diet()
        elif page == "Smoking by Gender":
            smoking_by_gender()
        elif page == "Clean Water by Region":
            water_by_region()


