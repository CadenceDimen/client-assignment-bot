import streamlit as st
from PIL import Image

# Inject custom CSS for Miami theme
st.markdown("""
    <style>
        body {
            background-color: #f0f8f5;
        }
        .big-title {
            font-size: 40px;
            color: #008C45;
            font-weight: 800;
            text-align: center;
        }
        .sub-text {
            font-size: 18px;
            color: #ff6600;
            text-align: center;
        }
        .button-style button {
            background-color: #ff6600;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            margin: 10px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Load and show logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.markdown('<div class="big-title">Client Assignment Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Helping you find the right team — the Miami way 🧡💚</div>', unsafe_allow_html=True)
st.markdown("---")

# Miami-themed buttons side by side
col1, col2, col3 = st.columns(3)
with col1:
    other_clicked = st.button("Other")
with col2:
    personal_clicked = st.button("Personal")
with col3:
    company_clicked = st.button("Company")

# Set session state
if other_clicked:
    st.session_state['filing_type'] = 'Other'
elif personal_clicked:
    st.session_state['filing_type'] = 'Just Personal'
elif company_clicked:
    st.session_state['filing_type'] = 'Company'

filing_type = st.session_state.get('filing_type', None)
st.markdown("---")

if filing_type == "Other":
    st.markdown("### 🧾 Trust Filing")
    grantor_type = st.radio("Is it a Grantor or Non-Grantor trust?", ["Grantor", "Non-Grantor"])
    st.success("📄 Fiduciary or Trust (6XXXXX)")

elif filing_type == "Just Personal":
    st.markdown("### 👤 Personal Filing")
    resident = st.radio("Are you a resident or have you been in the US longer than 365 days?", ["Yes", "No"])
    if resident == "Yes":
        foreign_assets = st.radio("Do you have foreign assets/entities/income?", ["Yes", "No"])
        if foreign_assets == "Yes":
            st.success("📄 US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons")
        else:
            st.success("📄 US Individual Tax Services (4XXXX) - Form 1040")
    else:
        itin = st.radio("Do you already have an ITIN?", ["Yes", "No"])
        if itin == "Yes":
            st.success("📄 NRA Individual Tax Services (4XXXX) - Form 1040NR")
        else:
            st.success("📄 NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on")

elif filing_type == "Company":
    st.markdown("### 🏢 Company Filing")
    entity_type = st.selectbox("What type of entity do you have?", ["Select", "Inc. or Corp.", "LLC"])
    if entity_type == "Inc. or Corp.":
        ownership = st.radio("Is the ownership US or Foreign?", ["US", "Foreign"])
        if ownership == "US":
            corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
            if corp_type == "C-Corp":
                st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120")
            else:
                st.success("📄 U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S")
        else:
            st.success("📄 Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F")

    elif entity_type == "LLC":
        owner_count = st.radio("How many owners are there?", ["1 Owner", "2+ Owners"])
        if owner_count == "1 Owner":
            residency = st.radio("Are you Foreign or U.S.?", ["Foreign", "U.S."])
            if residency == "Foreign":
                us_income = st.radio("Do you have operations in the U.S. or do you generate U.S.-based income?", ["Yes", "No"])
                if us_income == "No":
                    st.success("📄 Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120")
                else:
                    st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)")

            elif residency == "U.S.":
                elected = st.radio("Did you elect to be treated as a C-Corp or S-Corp?", ["Yes", "No"])
                if elected == "Yes":
                    corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
                    if corp_type == "C-Corp":
                        st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120")
                    else:
                        st.success("📄 U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S")
                else:
                    st.success("📄 US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)")
