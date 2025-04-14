import streamlit as st
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
import datetime
import Third  # Import Third.py for team matching

# Hide sidebar
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    label { font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# Force progress bar to start at exactly 60%
st.session_state["progress"] = 60
answered = 0

# Back button at the top
col_done, col_back = st.columns([1, 1])
with col_back:
    if st.button("🔙 Back"):
        st.switch_page("first.py")

# Title + intro
st.title("🎉 Thank You!")
st.write("Thank you for completing the survey!")
st.write("Now you are going to fill out some more information about the client so that they can automatically be placed on a team.")

# Client result from first page
client_result = st.session_state.get("client_result", "Not provided")

# Pricing and type mapping
price_ranges = {
    "U.S. Corporation with Tax Services (2XXXXX) - Form 1120": (2000, 2800),
    "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S": (2200, 3200),
    "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F": (2500, 3900),
    "U.S. Partnership with Tax Services (2XXXXX) - Form 1065": (2800, 3400),
    "Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)": (2800, 3600),
    "Non-Profit with Tax Services (2XXXXX)": (1800, 2600),
    "Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120": (1800, 2800),
    "US Individual Tax Services (4XXXX) - Form 1040": (1600, 2400),
    "NRA Individual Tax Services (4XXXX) - Form 1040NR": (1600, 2400),
    "Fiduciary or Trust (6XXXXX)": (2500, 3300),
    "Accounting Only - Any Company Type (7XXXXX)": (1200, 2000),
    "US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons": (1600, 2400),
    "NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on": (1600, 2400),
    "U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)": (2000, 2800),
    "US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)": (1600, 2400),
    "Consulting or One Time Project - NON-TAX (8XXXXX)": (1000, 2000)
}

client_id_map = {
    "U.S. Corporation with Tax Services (2XXXXX) - Form 1120": "1",
    "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S": "2",
    "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F": "3",
    "U.S. Partnership with Tax Services (2XXXXX) - Form 1065": "4",
    "Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)": "5",
    "Non-Profit with Tax Services (2XXXXX)": "6",
    "Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120": "7",
    "US Individual Tax Services (4XXXX) - Form 1040": "8",
    "NRA Individual Tax Services (4XXXX) - Form 1040NR": "9",
    "Fiduciary or Trust (6XXXXX)": "10",
    "Accounting Only - Any Company Type (7XXXXX)": "11",
    "US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons": "8a",
    "NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on": "9a",
    "U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)": "1a",
    "US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)": "8b",
    "Consulting or One Time Project - NON-TAX (8XXXXX)": "N/A"
}

# Collect inputs
language = st.radio("Language", ["English", "Spanish", "Portuguese"], index=None, key="language")
vip_status = st.radio("VIP Status", ["VIP", "Regular"], index=None, key="vip_status")
complexity = st.radio("Complexity", ["Low", "Medium", "High"], index=None, key="complexity")

if "estimate_changed" not in st.session_state:
    st.session_state.estimate_changed = False

def handle_slider_change():
    st.session_state.estimate_changed = True

price_min, price_max = price_ranges.get(client_result, (1000, 3000))
estimate = st.slider("Estimate", min_value=price_min, max_value=price_max, value=price_min, step=100, key="estimate", on_change=handle_slider_change)

unique_factor = st.text_input("Unique Factor", key="unique_factor")
client_tier = st.radio("Client Tier", ["1", "2", "3", "4", "5"], index=None, key="client_tier")
client_name = st.text_input("Client Name", key="client_name")
location = st.radio("Location", ["Coral Gables", "Brickell", "Aventura"], index=None, key="location")
referral_status = st.radio("Referral Status", ["Referral", "New Client"], index=None, key="referral_status")
month = st.radio("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=None, key="month")
previous_team = st.text_input("Previous Team", key="previous_team")
signed_proposal = st.radio("Signed Proposal", ["Yes", "No"], index=None, key="signed_proposal")

# Build DataFrame
client_id = client_id_map.get(client_result, "N/A")
client_data = {
    "Client ID Number": [client_id],
    "Client_Type": [client_result],
    "Client_Tier": [client_tier],
    "Client Name": [client_name],
    "Total Billing": [estimate],
    "Preferred_Location": [location],
    "Language": [language],
    "VIP": [vip_status],
    "Client Referral/New Client": [referral_status],
    "Month": [month],
    "If client referral what team before?": [previous_team],
    "Complexity": [complexity],
    "Signed Proposal": [signed_proposal],
    "Unique Factor": [unique_factor]
}
df = pd.DataFrame(client_data)

# Button to preview and run match
if st.button("🧾 Generate CSV"):
    st.markdown("### 📄 Generated CSV Preview")
    st.dataframe(df)
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="client_profile.csv",
        mime="text/csv"
    )

    # Pass to Third.py
    client_profile = df.iloc[0].to_dict()
    matched_names = Third.match_client_to_team(Third.latest_team_data, client_profile)
    matched_details = Third.get_team_details(Third.latest_team_data, matched_names)

    st.markdown("### ✅ Top 5 Team Matches")
    st.dataframe(matched_details)
