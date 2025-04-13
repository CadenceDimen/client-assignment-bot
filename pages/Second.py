import streamlit as st
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
import datetime

# Hide sidebar
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
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

# Language, VIP, Complexity
language = st.radio("What language does the client prefer?", ["English", "Spanish", "Portuguese"], index=None, key="language")
if language:
    answered += 1
vip_status = st.radio("Is the client a VIP or Regular?", ["VIP", "Regular"], index=None, key="vip_status")
if vip_status:
    answered += 1
complexity = st.radio("What is the complexity of the client?", ["Low", "Medium", "High"], index=None, key="complexity")
if complexity:
    answered += 1

# Show estimated billing slider with user interaction tracking
if "estimate_changed" not in st.session_state:
    st.session_state.estimate_changed = False

def handle_slider_change():
    st.session_state.estimate_changed = True

price_min, price_max = price_ranges.get(client_result, (1000, 3000))
estimate = st.slider(
    "💵 What is the estimated billing for this client?",
    min_value=price_min,
    max_value=price_max,
    value=price_min,
    step=100,
    key="estimate",
    on_change=handle_slider_change
)

if st.session_state.estimate_changed:
    answered += 1

# NEW FIELDS
st.markdown("---")
unique_factor = st.text_input("Unique Factor")
client_tier = st.selectbox("What is the client's tier?", ["", "1", "2", "3", "4", "5"])
client_name = st.text_input("What is the client's name?")
location = st.text_input("What is the client's preferred location?")
referral_status = st.radio("Client Referral / New Client", ["Referral", "New Client"], index=None)
month = st.selectbox("Month", ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
previous_team = st.text_input("If client referral, what team before?")
signed_proposal = st.radio("Signed Proposal", ["Yes", "No"], index=None)

# Total second page = 4 questions → 40 / 4 = 10% per question
progress = min(60 + (answered * 10), 100)
st.session_state["progress"] = progress
st.progress(progress / 100.0, text=f"Progress: {int(progress)}%")

# Get client ID
client_id = client_id_map.get(client_result, "N/A")

# Create and display DataFrame
client_data = {
    "Client ID Number": [client_id],
    "Client Type": [client_result],
    "Client Tier": [client_tier],
    "Client Name": [client_name],
    "Total Billing": [f"${estimate}"],
    "Location": [location],
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

# Display + download
st.markdown("### 📝 Summary of Selections:")
st.dataframe(df)
st.download_button(
    label="📅 Download Client Info as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='client_info.csv',
    mime='text/csv'
)

# Email sending section
SENDGRID_API_KEY = "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"
FROM_EMAIL = "cdimen@hco.com"

st.markdown("---")
st.markdown("### 📬 Send Proposal to Client")
recipient_email = st.text_input("Enter recipient's email address", key="recipient_email")

if st.button("📧 Send Proposal"):
    if recipient_email and "@" in recipient_email:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        b64_csv = base64.b64encode(csv_bytes).decode()

        message = Mail(
            from_email=Email(FROM_EMAIL, name="H&Co"),
            to_emails=To(recipient_email),
            subject="📄 Your Client Proposal from H&Co",
            plain_text_content=Content("text/plain", "Attached is the proposal with your estimated client details.")
        )

        attachment = Attachment()
        attachment.file_content = FileContent(b64_csv)
        attachment.file_type = FileType("text/csv")
        attachment.file_name = FileName("client_info.csv")
        attachment.disposition = Disposition("attachment")
        message.attachment = attachment

        try:
            sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            if response.status_code in [200, 202]:
                st.success(f"Proposal sent to {recipient_email} ✅")
            else:
                st.error("Something went wrong. Email not sent.")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
    else:
        st.warning("Please enter a valid email address.")

# Done button only
if st.button("✅ Done"):
    st.success("Client finalized!")
