import streamlit as st
from PIL import Image

# Inject custom CSS for Miami theme
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #333333;
            font-family: 'Open Sans', sans-serif;
        }
        .big-title {
            font-size: 40px;
            color: #003366;
            font-weight: 800;
            text-align: center;
        }
        .sub-text {
            font-size: 18px;
            color: #ff6600;
            text-align: center;
        }
        .stButton>button {
            background-color: #003366;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #002244;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Load and show logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.markdown('<div class="big-title">Client Assignment Bot</div>', unsafe_allow_html=True)
st.markdown("---")

# Button options for starting point
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Other"):
        st.session_state.clear()
        st.session_state['filing_type'] = 'Other'
with col2:
    if st.button("Personal"):
        st.session_state.clear()
        st.session_state['filing_type'] = 'Just Personal'
with col3:
    if st.button("Company"):
        st.session_state.clear()
        st.session_state['filing_type'] = 'Company'

filing_type = st.session_state.get('filing_type', None)
st.markdown("---")

# Progressive flow for COMPANY (LLC path)
if filing_type == "Company":
    st.markdown("### 🏢 Company Filing")

    entity_type = st.selectbox("What type of entity do you have?", ["", "Inc. or Corp.", "LLC"])
    if entity_type:
        st.session_state['company_entity'] = entity_type

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
        llc_owner_count = st.radio("How many owners are there?", ["1 Owner", "2+ Owners"])

        if llc_owner_count == "1 Owner":
            residency = st.radio("Are you Foreign or U.S.?", ["Foreign", "U.S."])
            if residency == "Foreign":
                us_income = st.radio("Do you have operations in the U.S. or do you generate U.S.-based income?", ["Yes", "No"])
                if us_income == "No":
                    st.success("📄 Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120")
                else:
                    st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)")
            else:
                elected = st.radio("Did you elect to be treated as a C-Corp or S-Corp?", ["Yes", "No"])
                if elected == "Yes":
                    corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
                    if corp_type == "C-Corp":
                        st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120")
                    else:
                        st.success("📄 U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S")
                else:
                    st.success("📄 US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)")

        elif llc_owner_count == "2+ Owners":
            structure = st.radio("Do you want to stay in a partnership or become a corporation?", ["Stay as a Partnership", "Become a Corporation", "Unsure"])
            if structure == "Stay as a Partnership":
                owners = st.radio("Are the owners US or Foreign?", ["US", "Foreign"])
                if owners == "US":
                    st.success("📄 U.S. Partnership with Tax Services (2XXXXX) - Form 1065")
                else:
                    st.success("📄 Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)")
            elif structure == "Become a Corporation":
                ownership = st.radio("Is the ownership US or Foreign?", ["US", "Foreign"])
                if ownership == "US":
                    corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
                    if corp_type == "C-Corp":
                        st.success("📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120")
                    else:
                        st.success("📄 U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S")
                else:
                    st.success("📄 Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F")
            else:
                st.success("📄 Consulting or One Time Project - NON-TAX (8XXXXX)\n\n📄 Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)\n📄 U.S. Corporation with Tax Services (2XXXXX) - Form 1120\n📄 Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F")

# Progressive flow for PERSONAL
if filing_type == "Just Personal":
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

# Progressive flow for OTHER
if filing_type == "Other":
    st.markdown("### 🧾 Trust Filing")
    grantor_type = st.radio("Is it a Grantor or Non-Grantor trust?", ["Grantor", "Non-Grantor"])
    st.success("📄 Fiduciary or Trust (6XXXXX)")
