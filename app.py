import streamlit as st

st.title("Client Assignment Bot")

st.write("Answer a few questions and we'll match you with the best team!")

industry = st.selectbox("What industry is your project in?", ["Finance", "Healthcare", "Tech", "Other"])
team_size = st.slider("Preferred team size:", 2, 6, 3)
priority = st.radio("What’s your top priority?", ["Experience", "Speed", "Availability"])

if st.button("Assign Me a Team"):
    if industry == "Finance" and priority == "Experience":
        team = "Team Alpha"
    else:
        team = "Team Beta"
    
    st.success(f"✅ You’ve been matched with **{team}**!")
