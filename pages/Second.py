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

# Language, VIP, Complexity
st.markdown('<p style="font-size:18px;"><b>What language does the client prefer?</b></p>', unsafe_allow_html=True)
language = st.radio("Language", ["English", "Spanish", "Portuguese"], index=None, key="language", label_visibility="collapsed")
if language:
    answered += 1

st.markdown('<p style="font-size:18px;"><b>Is the client a VIP or Regular?</b></p>', unsafe_allow_html=True)
vip_status = st.radio("VIP Status", ["VIP", "Regular"], index=None, key="vip_status", label_visibility="collapsed")
if vip_status:
    answered += 1

st.markdown('<p style="font-size:18px;"><b>What is the complexity of the client?</b></p>', unsafe_allow_html=True)
complexity = st.radio("Complexity", ["Low", "Medium", "High"], index=None, key="complexity", label_visibility="collapsed")
if complexity:
    answered += 1

# Estimated billing
if "estimate_changed" not in st.session_state:
    st.session_state.estimate_changed = False

def handle_slider_change():
    st.session_state.estimate_changed = True

price_min, price_max = price_ranges.get(client_result, (1000, 3000))

st.markdown('<p style="font-size:18px;"><b>💵 What is the estimated billing for this client?</b></p>', unsafe_allow_html=True)
estimate = st.slider("Estimate", min_value=price_min, max_value=price_max, value=price_min, step=100, key="estimate", on_change=handle_slider_change, label_visibility="collapsed")
if st.session_state.estimate_changed:
    answered += 1

# New fields
st.markdown('<p style="font-size:18px;"><b>Unique Factor</b></p>', unsafe_allow_html=True)
unique_factor = st.text_input("Unique Factor", key="unique_factor", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>What is the client\'s tier?</b></p>', unsafe_allow_html=True)
client_tier = st.radio("Client Tier", ["1", "2", "3", "4", "5"], index=None, key="client_tier", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>What is the client\'s name?</b></p>', unsafe_allow_html=True)
client_name = st.text_input("Client Name", key="client_name", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>What is the client\'s preferred location?</b></p>', unsafe_allow_html=True)
location = st.radio("Location", ["Coral Gables", "Brickell", "Aventura"], index=None, key="location", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>Is the client a referral or a new client?</b></p>', unsafe_allow_html=True)
referral_status = st.radio("Referral Status", ["Referral", "New Client"], index=None, key="referral_status", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>What month is the client joining?</b></p>', unsafe_allow_html=True)
month = st.radio("Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
], index=None, key="month", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>If the client is a referral, what team were they placed on before?</b></p>', unsafe_allow_html=True)
previous_team = st.text_input("Previous Team", key="previous_team", label_visibility="collapsed")

st.markdown('<p style="font-size:18px;"><b>Has the client signed the proposal?</b></p>', unsafe_allow_html=True)
signed_proposal = st.radio("Signed Proposal", ["Yes", "No"], index=None, key="signed_proposal", label_visibility="collapsed")

# Progress bar update
progress = min(60 + (answered * 10), 100)
st.session_state["progress"] = progress
st.progress(progress / 100.0, text=f"Progress: {int(progress)}%")

# Create and display DataFrame
client_id = client_id_map.get(client_result, "N/A")
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

# Email sending
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

# Done button
if st.button("✅ Done"):
    st.success("Client finalized!")
