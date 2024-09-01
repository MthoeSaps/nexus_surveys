import streamlit as st
import pandas as pd
import os
import plotly.express as px
import time
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="N.E.X.U.S Survey", initial_sidebar_state="expanded", page_icon="📝", layout="centered")

# Define the CSV file path
csv_file_path = os.path.expanduser("nexus_surveys/databases/nexus_survey_data/responses.csv")

# Create the directory if it doesn't exist
csv_dir = os.path.dirname(csv_file_path)
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(csv_file_path):
    headers = [
        "timestamp", "suburb", "gender", "employment_status", "age", "challenges", "improvements", 
        "key_assets", "leverage_strengths", "land_use", "zoning_feedback", 
        "housing_needs", "mix_housing_options", "transport_improvements", 
        "sustainable_mobility", "commercial_support", "maximize_benefits", 
        "environmental_concerns", "sustainable_design", "engagement_methods", 
        "fostering_ownership"
    ]
    pd.DataFrame(columns=headers).to_csv(csv_file_path, index=False)

# Load suburbs from an Excel file
suburbs_file_path = "nexus_surveys/database/suburbs.xlsx"
suburbs = []
if os.path.exists(suburbs_file_path):
    df = pd.read_excel(suburbs_file_path)
    suburbs = df['suburb'].dropna().tolist()  # Ensure 'Suburb' column exists

if not suburbs:
    st.error("No suburbs available for selection. Please check the suburbs file.")
else:
    # Title of the app
    st.title("🧠:blue[Nexus] Community Survey")
    col1, col2 = st.columns([5, 3])
    col1.write("*- Software developed by Mthoe Saps Construction technologies*")
    col2.write("*- Prototype developed on 30-08-2024*")
    st.divider()

    # Participant Information
    st.header("Participant :blue[Information]")
    suburb = st.selectbox("Select your suburb of residence:", suburbs)
    gender = st.radio("Select your gender:", ["Male", "Female", "Non-binary", "Prefer not to say"])
    employment_status = st.radio("Select your employment status:", ["Employed", "Unemployed", "Self-employed", "Student"])
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

    # Community Needs and Priorities
    st.header("1. Community :blue[Needs] and :blue[Priorities]")
    challenges = st.multiselect(
        "a. What are the biggest challenges or pain points that the community wants the Nexus project to address?",
        ["Lack of infrastructure", "High unemployment", "Poor public transportation", "Housing affordability", 
         "Water shortages", "Health service access", "Education quality", "Environmental degradation"]
    )
    improvements = st.multiselect(
        "b. What type of improvements or enhancements would residents most likely like to see in the project area?",
        ["Better road networks", "Improved public transit", "Community parks", "Affordable housing", 
         "Access to clean water", "Healthcare facilities", "Wi-Fi hotspots", "Job training programs"]
    )

    # Existing Community Assets
    st.header("2. Existing :blue[Community] Assets")
    key_assets = st.multiselect(
        "a. What are the key community assets, infrastructure, and resources that Nexus should seek to provide, preserve, and build upon?",
        ["Schools", "Community centers", "Healthcare facilities", "Local markets", 
         "Public parks", "Cultural heritage sites", "Transport links", "Small businesses"]
    )
    leverage_strengths = st.multiselect(
        "b. How can the project leverage the existing strengths and character of the neighborhood/development area?",
        ["Promote local businesses", "Enhance community events", "Preserve cultural heritage", 
         "Improve public spaces", "Encourage local art and culture", "Strengthen community networks"]
    )

    # Land Use and Development Preferences
    st.header("3. :blue[Land Use] and Development Preferences")
    land_use = st.radio(
        "a. What type of land use do community members want to see?",
        ["Residential", "Commercial", "Mixed Use", "Industrial", "Agricultural"]
    )
    zoning_feedback = st.multiselect(
        "b. How do you feel about the proposed zoning challenges, densities, and building heights for the project area?",
        ["Supportive of higher densities", "Prefer low-rise buildings", "Concerned about traffic impact", 
         "Need more green spaces", "Desire mixed-use developments", "Other"]
    )

    # Housing and Affordability
    st.header("4. Housing and :blue[Affordability]")
    housing_needs = st.multiselect(
        "a. What are the community's needs and priorities when it comes to housing types, sizes, and affordability levels?",
        ["Low-cost housing", "Medium-density apartments", "Single-family homes", "Shared accommodations", 
         "Student housing", "Elderly housing"]
    )
    mix_housing_options = st.multiselect(
        "b. How can the Nexus development plan ensure an appropriate mix of housing options to meet diverse needs?",
        ["Incorporate affordable units", "Include varied sizes", "Ensure accessibility", 
         "Focus on sustainable designs", "Engage local builders", "Promote community input"]
    )

    # Connectivity and Mobility
    st.header("5. Connectivity :blue[and] Mobility")
    transport_improvements = st.multiselect(
        "a. What transportation improvements do community members feel are the most important?",
        ["Paved roads", "Public bus services", "Bicycle lanes", "Footpaths", 
         "Taxi services", "Improved airport facilities"]
    )
    sustainable_mobility = st.multiselect(
        "b. How can the Nexus project promote sustainable, equitable, and accessible mobility options?",
        ["Expand public transport", "Encourage carpooling", "Develop bike-sharing programs", 
         "Improve pedestrian safety", "Implement traffic calming measures", "Promote electric vehicles"]
    )

    # Economic Development and Community Benefits
    st.header("6. :blue[Economic] Development and :blue[Community] Benefits")
    commercial_support = st.multiselect(
        "a. What type of commercial/retail uses, employment opportunities, or economic initiatives would the community support?",
        ["Local markets", "Small and medium enterprises (SMEs)", "Job training programs", 
         "Retail shops", "Agricultural initiatives", "Tourism development"]
    )
    maximize_benefits = st.multiselect(
        "b. How can the Nexus plan maximize economic benefits and job creation for residents?",
        ["Support local entrepreneurship", "Create training programs", "Foster partnerships with local businesses", 
         "Attract investment", "Promote tourism", "Ensure fair wages"]
    )

    # Sustainability and Environmental Impact
    st.header("7. Sustainability and :blue[Environmental] Impact")
    environmental_concerns = st.multiselect(
        "a. What are the community's key concerns regarding the environmental impact of the Nexus project?",
        ["Water pollution", "Deforestation", "Waste management", "Air quality", 
         "Loss of biodiversity", "Climate change adaptation"]
    )
    sustainable_design = st.multiselect(
        "b. How can the plan incorporate sustainable design, energy efficiency, and green infrastructure?",
        ["Use of renewable energy", "Green building materials", "Water conservation measures", 
         "Community gardens", "Urban forestry", "Recycling programs"]
    )

    # Community Engagement and Ownership
    st.header("8. Community :blue[Engagement] and :blue[Ownership]")
    engagement_methods = st.multiselect(
        "a. How can the Nexus project efficiently engage and collaborate with the local community throughout the process?",
        ["Community workshops", "Online surveys", "Public meetings", "Social media engagement", 
         "Partnerships with local organizations", "Feedback sessions"]
    )
    fostering_ownership = st.multiselect(
        "b. What ideas do community members have for fostering a sense of ownership and stewardship over Nexus initiatives?",
        ["Community-led projects", "Volunteer opportunities", "Local advisory boards", 
         "Regular updates and transparency", "Celebrating local culture", "Educational programs"]
    )

    # Submit Button
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Submit Survey"):
            # Collect all responses
            response_data = {
                "timestamp": datetime.now().isoformat(),
                "suburb": suburb,
                "gender": gender,
                "employment_status": employment_status,
                "age": age,
                "challenges": ', '.join(challenges),
                "improvements": ', '.join(improvements),
                "key_assets": ', '.join(key_assets),
                "leverage_strengths": ', '.join(leverage_strengths),
                "land_use": land_use,
                "zoning_feedback": ', '.join(zoning_feedback),
                "housing_needs": ', '.join(housing_needs),
                "mix_housing_options": ', '.join(mix_housing_options),
                "transport_improvements": ', '.join(transport_improvements),
                "sustainable_mobility": ', '.join(sustainable_mobility),
                "commercial_support": ', '.join(commercial_support),
                "maximize_benefits": ', '.join(maximize_benefits),
                "environmental_concerns": ', '.join(environmental_concerns),
                "sustainable_design": ', '.join(sustainable_design),
                "engagement_methods": ', '.join(engagement_methods),
                "fostering_ownership": ', '.join(fostering_ownership)
            }
            
            # Load existing data and append the new response
            df = pd.read_csv(csv_file_path)
            df.loc[len(df)] = response_data 
            df.to_csv(csv_file_path, index=False)

            st.markdown(
                """
                <div style="border: 2px solid blue; background-color: orange; padding: 10px; border-radius: 5px; margin-top: 20px;">
                    <strong>Thank you for your responses!</strong> Your feedback has been recorded.
                </div>
                """,
                unsafe_allow_html=True
            ) 
            #st.toast("Thank you for your responses! Your feedback has been recorded.")
            #time.sleep(10)
    
    with col2:
        st.empty()
        #if st.button("Clear Fields"):
         #   st.session_state.clear()
          #  st.experimental_rerun()

    st.divider()
    
    st.info("If you are interested in gaining understanding of the survey data, follow our social media platforms and also our main blog page.")
    
with st.sidebar:
    # Display Nexus logo
    image_path = "nexus_surveys/images/logo9.png"
    image = Image.open(image_path)
    with st.container(border=True):
        st.image(image, caption="N.E.X.U.S trademark logo.", width=240)
    st.subheader("About Nexus", divider=True)

    with st.expander("Overview 🌍"):
        st.write(
            "The **Nexus Community Survey** is an initiative aimed at gathering valuable insights from residents of Bulawayo regarding land development and community needs. "
            "This interactive survey allows community members to express their thoughts on various topics."
        )
    
    with st.expander("Purpose 🎯"):
        st.write(
            "The data collected through this survey will help Nexus and local authorities make informed decisions that align with the community’s priorities and aspirations. "
            "By participating, you contribute to shaping a better future for Bulawayo."
        )
    
    with st.expander("How It Works ⚙️"):
        st.write(
            "1. **Select Your Suburb**: Choose your area of residence from a dropdown list.\n"
            "2. **Answer Questions**: Respond to questions regarding your challenges, preferences, and suggestions.\n"
            "3. **Submit Your Feedback**: Once completed, submit your responses, which will be recorded for analysis."
        )
    
    with st.expander("Community Challenges 🚧"):
        st.write(
            "This section allows residents to identify the biggest issues facing their neighborhoods, such as:\n"
            "- Lack of infrastructure\n"
            "- High unemployment\n"
            "- Poor public transportation\n"
            "- Housing affordability\n"
            "- Water shortages\n"
            "- Health service access\n"
            "- Education quality\n"
            "- Environmental degradation\n"
            "Your feedback on these challenges will help prioritize community development efforts."
        )

    with st.expander("Economic Opportunities 💼"):
        st.write(
            "Community members can voice their opinions on commercial developments and initiatives that could enhance local economic growth, such as:\n"
            "- Support for local markets\n"
            "- Development of small and medium enterprises (SMEs)\n"
            "- Job training programs\n"
            "- Retail shops\n"
            "- Agricultural initiatives\n"
            "- Tourism development\n"
            "By sharing your thoughts, you can help shape economic policies that benefit the community."
        )
    
    with st.expander("Participation 🙌"):
        st.write(
            "Your voice matters! Thank you for taking the time to participate in this important initiative."
        )
    
    with st.container(border=True):
        st.subheader("Get in touch with us📞", divider=True)
        selected_option = st.selectbox("Select Contact Method", ["WhatsApp", "LinkedIn", "Instagram"])
        if selected_option == "WhatsApp":
            st.info("Use the following buttons to get in touch with us:")
            st.link_button("WhatsApp Us", "https://wa.me/263777932721")
        if selected_option == "LinkedIn":
            st.info("You can visit our LinkedIn profile and check our work, you can also contact us from there")
            st.link_button("View our LinkedIn Profile", "https://www.linkedin.com/in/mthokozisi-sapuwa-1ab2151ab?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")
        if selected_option == "Instagram":
            st.info("Find us on IG too")
            st.link_button("Instagram Chat", "https://www.instagram.com/mthoe_saps_construction_tech?igsh=MWZibnVpOWZkcmcyNg==")
