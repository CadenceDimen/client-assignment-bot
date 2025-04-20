import streamlit as st
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
import datetime
import Third  # Import Third.py for team matching
from powerbi_push import push_to_power_bi


# Hide sidebar
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    label { font-size: 20px !important; }

    /* Sticky progress bar styling */
    .sticky-progress-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        width: 100%;
        z-index: 9999;
        background-color: white;
        padding: 0.5rem 1rem;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }

    /* Ensure main content has top padding to avoid being hidden behind sticky bar */
    .block-container {
        padding-top: 80px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Set starting progress
if "progress" not in st.session_state:
    st.session_state["progress"] = 60  # Start at 60% after First.py

# Total questions in Second.py
total_questions = 12  # adjust if you add/remove questions
step = 40 / total_questions

# Sticky custom progress bar
st.markdown('<div class="sticky-progress-container">', unsafe_allow_html=True)
st.progress(st.session_state["progress"] / 100.0, text=f"Progress: {int(st.session_state['progress'])}%")
st.markdown('</div>', unsafe_allow_html=True)

# Back button
col_done, col_back = st.columns([1, 1])
with col_back:
    if st.button("🔙 Back"):
        st.switch_page("first.py")

# Title
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
st.radio("Language", ["English", "Spanish", "Portuguese"], index=None, key="language")
st.radio("VIP Status", ["VIP", "Regular"], index=None, key="vip_status")
st.radio("Complexity", ["Low", "Medium", "High"], index=None, key="complexity")

if "estimate_changed" not in st.session_state:
    st.session_state.estimate_changed = False

def handle_slider_change():
    st.session_state.estimate_changed = True

price_min, price_max = price_ranges.get(client_result, (1000, 3000))
st.slider("Estimate", min_value=price_min, max_value=price_max, value=price_min, step=100, key="estimate", on_change=handle_slider_change)
st.text_input("Unique Factor", key="unique_factor")
st.radio("Client Tier", ["1", "2", "3", "4", "5"], index=None, key="client_tier")
st.text_input("Client Name", key="client_name")
st.radio("Location", ["Coral Gables", "Brickell", "Aventura"], index=None, key="location")
st.radio("Referral Status", ["Referral", "New Client"], index=None, key="referral_status")
st.radio("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=None, key="month")
st.text_input("Previous Team", key="previous_team")
st.radio("Signed Proposal", ["Yes", "No"], index=None, key="signed_proposal")

# Update top progress bar only based on answered fields
fields = [
    "language", "vip_status", "complexity", "estimate", "unique_factor",
    "client_tier", "client_name", "location", "referral_status",
    "month", "previous_team", "signed_proposal"
]
answered = sum(1 for field in fields if st.session_state.get(field) not in [None, ""])
new_progress = min(round(60 + answered * step), 100)
st.session_state["progress"] = new_progress
st.markdown("""
    <script>
        const topBar = window.parent.document.querySelector('.sticky-progress-container');
        if (topBar) topBar.scrollIntoView({ behavior: 'smooth', block: 'start' });
    </script>
""", unsafe_allow_html=True)

# Build DataFrame
client_id = client_id_map.get(client_result, "N/A")
client_data = {
    "Client ID Number": [client_id],
    "Client_Type": [client_result],
    "Client_Tier": [st.session_state.get("client_tier")],
    "Client Name": [st.session_state.get("client_name")],
    "Total Billing": [st.session_state.get("estimate")],
    "Preferred_Location": [st.session_state.get("location")],
    "Language": [st.session_state.get("language")],
    "VIP": [st.session_state.get("vip_status")],
    "Client Referral/New Client": [st.session_state.get("referral_status")],
    "Month": [st.session_state.get("month")],
    "If client referral what team before?": [st.session_state.get("previous_team")],
    "Complexity": [st.session_state.get("complexity")],
    "Signed Proposal": [st.session_state.get("signed_proposal")],
    "Unique Factor": [st.session_state.get("unique_factor")]
}
df = pd.DataFrame(client_data)

# Button to preview and run match
if st.button("📟 Generate CSV"):
    st.markdown("### 📄 Generated CSV Preview")
    st.dataframe(df)
    st.download_button(
        label="📅 Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="client_profile.csv",
        mime="text/csv"
    )

    client_profile = df.iloc[0].to_dict()
    matched_names = Third.match_client_to_team(Third.latest_team_data, client_profile)

    #from powerbi_push import push_to_power_bi  # Add this at the top of your file if you haven’t
    #if matched_names:
    #    top_team = matched_names[0]
    #    push_to_power_bi(client_type=client_result, team=top_team)

    matched_details = Third.get_team_details(Third.latest_team_data, matched_names)

    st.markdown("### ✅ Top Team Assignments")
    st.dataframe(matched_details)
