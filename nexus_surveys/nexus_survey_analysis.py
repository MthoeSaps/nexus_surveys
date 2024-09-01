import streamlit as st
import pandas as pd
import os
from PIL import Image
import plotly.express as px

st.set_page_config(page_title="N.E.X.U.S Survey Analysis", initial_sidebar_state="expanded", page_icon="🧠", layout="wide")

# Define the CSV file path
csv_file_path = os.path.expanduser("nexus_surveys/databases/nexus_survey_data/responses.csv")

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    # Create an empty DataFrame if the file does not exist
    df = pd.DataFrame(columns=[
        "timestamp", "suburb", "gender", "age", "challenges", "improvements", 
        "key_assets", "leverage_strengths", "land_use", "zoning_feedback", 
        "housing_needs", "mix_housing_options", "transport_improvements", 
        "sustainable_mobility", "commercial_support", "maximize_benefits", 
        "environmental_concerns", "sustainable_design", "engagement_methods", 
        "fostering_ownership"
    ])
    df.to_csv(csv_file_path, index=False)
else:
    # Load the data from the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert relevant columns to strings and fill NaN values
    columns_to_convert = [
        'challenges', 'improvements', 'key_assets', 
        'leverage_strengths', 'land_use', 'zoning_feedback', 
        'housing_needs', 'transport_improvements', 
        'environmental_concerns', 'engagement_methods'
    ]

    # Convert all specified columns to string type
    for column in columns_to_convert:
        df[column] = df[column].astype(str).fillna('')

    # Convert 'age' column to numeric and handle NaN values
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

# Custom CSS for metrics styling
st.markdown("""
<style>
.metric-card {
    border: 2px solid #1e90ff; /* Blue border */
    border-radius: 8px; /* Rounded corners */
    background-color: #e0f7fa; /* Light blue background */
    padding: 15px;
    text-align: center;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title of the app
col1, col2 = st.columns([5, 2])
with st.container(border=False):
    col1.title("🧠:blue[Nexus] Community Survey Analysis Platform")
with st.container(border=False):
    col1.subheader(":blue[Analyze our Bulawayo Land Development survey] data here on our research dashboard", divider=False)
    col1.write("The data is modeled through our :blue[Data Science Algorithms found on our Nexus Engine].")

# Display nexus logo
image_path = "nexus_surveys/images/logo9.png"
image = Image.open(image_path)
with st.container(border=False):
    col2.image(image, caption="N.E.X.U.S trademark logo.", width=240)

st.divider()

# Display metrics
total_responses = len(df)
total_unique_suburbs = df['suburb'].nunique()
average_age = int(df['age'].mean()) if not df['age'].isnull().all() else 0
total_challenges = df['challenges'].str.split(', ').explode().nunique()
total_improvements = df['improvements'].str.split(', ').explode().nunique()

# Styled metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    with st.container():
        st.markdown('<div class="metric-card">Total Responses: {}</div>'.format(total_responses), unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="metric-card">Unique Suburbs: {}</div>'.format(total_unique_suburbs), unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="metric-card">Average Age: {}</div>'.format(average_age), unsafe_allow_html=True)

with col4:
    with st.container():
        st.markdown('<div class="metric-card">Total Challenges: {}</div>'.format(total_challenges), unsafe_allow_html=True)

with col5:
    with st.container():
        st.markdown('<div class="metric-card">Total Improvements: {}</div>'.format(total_improvements), unsafe_allow_html=True)

# Display the raw data
st.header("Raw :blue[Data]")
st.write(df)

# Buttons for deleting last entry and clearing database
col1, col2 = st.columns(2)

with col1:
    if st.button(":blue[Delete Last Entry]"):
        if len(df) > 0:
            df = df[:-1]  # Remove the last entry
            df.to_csv(csv_file_path, index=False)
            st.success("Last entry deleted.")
        else:
            st.warning("No entries to delete.")

with col2:
    if st.button(":orange[Clear Database]"):
        df = pd.DataFrame(columns=columns_to_convert)
        df.to_csv(csv_file_path, index=False)
        st.success("Database cleared.")

# Function to filter data based on user selection
def filter_data(column, selected_options):
    if selected_options:
        if df[column].dtype in ['int64', 'float64']:
            return df[df[column].isin(selected_options)]
        else:
            selected_options = [str(option) for option in selected_options]
            return df[df[column].astype(str).str.contains('|'.join(selected_options), na=False)]
    return df

# Summary Statistics
st.divider()
st.header(":blue[Summary] Statistics")

# Age Distribution
st.subheader("Age Distribution")
age_filter = st.multiselect("Select Age Groups:", options=df['age'].unique(), default=df['age'].unique())
filtered_age_data = filter_data('age', age_filter)

# Bar chart for Age Distribution
if not filtered_age_data.empty:
    st.bar_chart(filtered_age_data['age'].value_counts().sort_index())
else:
    st.warning("No data available for the selected age groups.")

# Pie chart for Age Distribution
if not filtered_age_data.empty:
    age_counts = filtered_age_data['age'].value_counts()
    fig = px.pie(age_counts, values=age_counts.values, names=age_counts.index, 
                  title="Age Distribution", hover_data=[age_counts.index])
    st.plotly_chart(fig)
else:
    st.warning("No data available for the selected age groups.")

# Challenges Analysis
st.subheader("Challenges Identified")
challenges_filter = st.multiselect("Select Challenges:", options=df['challenges'].str.get_dummies(sep=', ').columns.tolist())
filtered_challenges_data = filter_data('challenges', challenges_filter)
if not filtered_challenges_data.empty:
    challenges = filtered_challenges_data['challenges'].str.get_dummies(sep=', ')
    st.bar_chart(challenges.sum())
else:
    st.warning("No data available for the selected challenges.")

# Improvements Analysis
st.subheader("Improvements Suggested")
improvements_filter = st.multiselect("Select Improvements:", options=df['improvements'].str.get_dummies(sep=', ').columns.tolist())
filtered_improvements_data = filter_data('improvements', improvements_filter)
if not filtered_improvements_data.empty:
    improvements = filtered_improvements_data['improvements'].str.get_dummies(sep=', ')
    st.bar_chart(improvements.sum())
else:
    st.warning("No data available for the selected improvements.")

# Key Assets Analysis
st.subheader("Key Community Assets")
key_assets_filter = st.multiselect("Select Key Assets:", options=df['key_assets'].str.get_dummies(sep=', ').columns.tolist())
filtered_key_assets_data = filter_data('key_assets', key_assets_filter)
if not filtered_key_assets_data.empty:
    key_assets = filtered_key_assets_data['key_assets'].str.get_dummies(sep=', ')
    st.bar_chart(key_assets.sum())
else:
    st.warning("No data available for the selected key assets.")

# Leverage Strengths Analysis
st.subheader("Leverage Strengths")
leverage_strengths_filter = st.multiselect("Select Strengths:", options=df['leverage_strengths'].str.get_dummies(sep=', ').columns.tolist())
filtered_leverage_strengths_data = filter_data('leverage_strengths', leverage_strengths_filter)
if not filtered_leverage_strengths_data.empty:
    leverage_strengths = filtered_leverage_strengths_data['leverage_strengths'].str.get_dummies(sep=', ')
    st.bar_chart(leverage_strengths.sum())
else:
    st.warning("No data available for the selected strengths.")

# Land Use Preferences
st.subheader("Land Use Preferences")
land_use_filter = st.multiselect("Select Land Use:", options=df['land_use'].unique())
filtered_land_use_data = filter_data('land_use', land_use_filter)
if not filtered_land_use_data.empty:
    land_use_counts = filtered_land_use_data['land_use'].value_counts()
    st.bar_chart(land_use_counts)
else:
    st.warning("No data available for the selected land use preferences.")

# Zoning Feedback
st.subheader("Zoning Feedback")
zoning_feedback_filter = st.multiselect("Select Zoning Feedback:", options=df['zoning_feedback'].str.get_dummies(sep=', ').columns.tolist())
filtered_zoning_data = filter_data('zoning_feedback', zoning_feedback_filter)
if not filtered_zoning_data.empty:
    zoning_feedback_counts = filtered_zoning_data['zoning_feedback'].str.get_dummies(sep=', ').sum()
    st.bar_chart(zoning_feedback_counts)
else:
    st.warning("No data available for the selected zoning feedback.")

# Housing Needs Analysis
st.subheader("Housing Needs")
housing_needs_filter = st.multiselect("Select Housing Needs:", options=df['housing_needs'].str.get_dummies(sep=', ').columns.tolist())
filtered_housing_needs_data = filter_data('housing_needs', housing_needs_filter)
if not filtered_housing_needs_data.empty:
    housing_needs = filtered_housing_needs_data['housing_needs'].str.get_dummies(sep=', ')
    st.bar_chart(housing_needs.sum())
else:
    st.warning("No data available for the selected housing needs.")

# Transport Improvements
st.subheader("Transport Improvements")
transport_improvements_filter = st.multiselect("Select Transport Improvements:", options=df['transport_improvements'].str.get_dummies(sep=', ').columns.tolist())
filtered_transport_data = filter_data('transport_improvements', transport_improvements_filter)
if not filtered_transport_data.empty:
    transport_improvements = filtered_transport_data['transport_improvements'].str.get_dummies(sep=', ')
    st.bar_chart(transport_improvements.sum())
else:
    st.warning("No data available for the selected transport improvements.")

# Environmental Concerns
st.subheader("Environmental Concerns")
environmental_concerns_filter = st.multiselect("Select Environmental Concerns:", options=df['environmental_concerns'].str.get_dummies(sep=', ').columns.tolist())
filtered_environmental_data = filter_data('environmental_concerns', environmental_concerns_filter)
if not filtered_environmental_data.empty:
    environmental_concerns = filtered_environmental_data['environmental_concerns'].str.get_dummies(sep=', ')
    st.bar_chart(environmental_concerns.sum())
else:
    st.warning("No data available for the selected environmental concerns.")

# Community Engagement Methods
st.subheader("Engagement Methods")
engagement_methods_filter = st.multiselect("Select Engagement Methods:", options=df['engagement_methods'].str.get_dummies(sep=', ').columns.tolist())
filtered_engagement_data = filter_data('engagement_methods', engagement_methods_filter)
if not filtered_engagement_data.empty:
    engagement_methods = filtered_engagement_data['engagement_methods'].str.get_dummies(sep=', ')
    st.bar_chart(engagement_methods.sum())
else:
    st.warning("No data available for the selected engagement methods.")
