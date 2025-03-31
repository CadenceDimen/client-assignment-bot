import streamlit as st
from PIL import Image

# Load and show logo
logo = Image.open("logo.png")
st.image(logo, use_column_width=True)

st.title("Client Assignment Bot")

# Step 1: What are you filing for?
filing_type = st.selectbox("What are you filing for?", ["Select", "Other", "Just Personal", "Company"])

if filing_type == "Other":
    trust = st.radio("Is it for a trust?", ["Yes", "No"])
    if trust == "Yes":
        grantor_type = st.radio("Is it a Grantor or Non-Grantor trust?", ["Grantor", "Non-Grantor"])
        income_type = st.radio("Are you earning income continuously or one-time?", ["One-time", "Continuously"])
        if income_type == "One-time":
            st.success("📄 Project - One Time Filing - Trust 1041 (8XXXXX)\n\n🖨️ Engagement Letter: '18 - ONE TIME Trust 1041'")
        else:
            st.success("📄 Fiduciary or Trust (6XXXXX)\n\n🖨️ Engagement Letter: '10 - Fiduciary or Trust'")

elif filing_type == "Just Personal":
    resident = st.radio("Are you a resident or have you been in the US longer than 365 days?", ["Yes", "No"])
    if resident == "Yes":
        foreign_assets = st.radio("Do you have foreign assets/entities/income?", ["Yes", "No"])
        income_type = st.radio("Are you earning income continuously or one-time?", ["One-time", "Continuously"])
        if foreign_assets == "Yes":
            if income_type == "One-time":
                st.success("📄 Project - One Time Filing - US Individual Form 1040 (8XXXXX) with foreign add-ons\n\n🖨️ Engagement Letter: '21 - ONE TIME Form 1040 - Foreign add-ons'")
            else:
                st.success("📄 US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons\n\n🖨️ Engagement Letter: '22 - Form 1040 - Foreign add-ons'")
        else:
            if income_type == "One-time":
                st.success("📄 Project - One Time Filing - US Individual Form 1040 (8XXXXX)\n\n🖨️ Engagement Letter: '19 - ONE TIME US Individual Form 1040'")
            else:
                st.success("📄 US Individual Tax Services (4XXXX) - Form 1040\n\n🖨️ Engagement Letter: '8 - Form 1040'")
    else:
        itin = st.radio("Do you already have an ITIN?", ["Yes", "No"])
        income_type = st.radio("Are you earning income continuously or one-time?", ["One-time", "Continuously"])
        if itin == "Yes":
            if income_type == "One-time":
                st.success("📄 Project - One Time Filing - NRA Individual Form 1040NR (8XXXXX)\n\n🖨️ Engagement Letter: '20 - ONE TIME NRA Individual Form 1040NR'")
            else:
                st.success("📄 NRA Individual Tax Services (4XXXX) - Form 1040NR\n\n🖨️ Engagement Letter: '9 - Form 1040NR'")
        else:
            if income_type == "One-time":
                st.success("📄 Project - One Time Filing - NRA Individual Form 1040NR (8XXXXX) with W7 add-on\n\n🖨️ Engagement Letter: '23 - ONE TIME Form 1040 NR (W7 add-on)'")
            else:
                st.success("📄 NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on\n\n🖨️ Engagement Letter: '24 - Form 1040 NR (W7 add-on)'")

elif filing_type == "Company":
    entity_type = st.selectbox("What type of entity do you have?", ["Select", "Inc. or Corp.", "LLC"])
    if entity_type == "Inc. or Corp.":
        ownership = st.radio("Is the ownership US or Foreign?", ["US", "Foreign"])
        if ownership == "US":
            corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
            income_type = st.radio("Are you earning income continuously or one-time?", ["One-time", "Continuously"])
            if corp_type == "C-Corp":
                if income_type == "One-time":
                    st.success("📄 Project - One Time Filing - C-Corp Tax Form 1120 (8XXXXX)\n\n🖨️ Engagement Letter: '13 - ONE TIME C-Corp Tax Form 1120'")
                else:
                    st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120\n\n🖨️ Engagement Letter: '1 - Form 1120'")
            else:
                if income_type == "One-time":
                    st.success("📄 Project - One Time Filing - S-Corp Tax 1120-S (8XXXXX)\n\n🖨️ Engagement Letter: '14 - ONE TIME S-Corp Tax 1120-S'")
                else:
                    st.success("📄 U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S\n\n🖨️ Engagement Letter: '2 - Form 1120-S'")
        else:
            income_type = st.radio("Are you earning income continuously or one-time?", ["One-time", "Continuously"])
            if income_type == "One-time":
                st.success("📄 Project - One Time Filing - Foreign Co Tax 1120-F (8XXXXX)\n\n🖨️ Engagement Letter: '15 - ONE TIME Foreign Co Tax 1120-F'")
            else:
                st.success("📄 Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F\n\n🖨️ Engagement Letter: '3 - Form 1120-F'")
