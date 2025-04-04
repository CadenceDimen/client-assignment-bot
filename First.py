import streamlit as st
from PIL import Image

# Hide sidebar
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

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
        .stButton>button {
            background-color: #003366;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #002244;
        }
    </style>
""", unsafe_allow_html=True)

# Logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.markdown('<div class="big-title">Client Assignment Bot</div>', unsafe_allow_html=True)
st.markdown("---")

# Initial buttons
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

show_done = False  # triggers visibility of done button

# ------------------------
# Company Flow
# ------------------------
if filing_type == "Company":
    st.markdown("### 🏢 Company Filing")
    entity_type = st.selectbox("What type of entity do you have?", ["", "Inc. or Corp.", "LLC"])

    if entity_type == "Inc. or Corp.":
        ownership = st.radio("Is the ownership US or Foreign?", ["US", "Foreign"])
        if ownership == "US":
            corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
            if corp_type == "C-Corp":
                result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
            else:
                result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
        else:
            result = "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F"
        st.session_state["client_result"] = result
        st.success(f"📄 {result}")
        show_done = True

    elif entity_type == "LLC":
        owners = st.radio("How many owners are there?", ["1 Owner", "2+ Owners"])
        if owners == "1 Owner":
            residency = st.radio("Are you Foreign or U.S.?", ["Foreign", "U.S."])
            if residency == "Foreign":
                has_us_income = st.radio("Do you have operations in the U.S. or U.S.-based income?", ["Yes", "No"])
                if has_us_income == "No":
                    result = "Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120"
                else:
                    result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)"
            else:
                elected = st.radio("Did you elect to be treated as a C-Corp or S-Corp?", ["Yes", "No"])
                if elected == "Yes":
                    corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
                    if corp_type == "C-Corp":
                        result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
                    else:
                        result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
                else:
                    result = "US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)"
            st.session_state["client_result"] = result
            st.success(f"📄 {result}")
            show_done = True

        elif owners == "2+ Owners":
            structure = st.radio("Do you want to stay in a partnership or become a corporation?", ["Stay as a Partnership", "Become a Corporation", "Unsure"])
            if structure == "Stay as a Partnership":
                owner_type = st.radio("Are the owners US or Foreign?", ["US", "Foreign"])
                if owner_type == "US":
                    result = "U.S. Partnership with Tax Services (2XXXXX) - Form 1065"
                else:
                    result = "Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)"
            elif structure == "Become a Corporation":
                corp_owner = st.radio("Is the ownership US or Foreign?", ["US", "Foreign"])
                if corp_owner == "US":
                    corp_type = st.radio("Is it a C-Corp or S-Corp?", ["C-Corp", "S-Corp"])
                    if corp_type == "C-Corp":
                        result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
                    else:
                        result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
                else:
                    result = "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F"
            else:
                result = "Consulting or One Time Project - NON-TAX (8XXXXX)"
            st.session_state["client_result"] = result
            st.success(f"📄 {result}")
            show_done = True

# ------------------------
# Personal Flow
# ------------------------
elif filing_type == "Just Personal":
    st.markdown("### 👤 Personal Filing")
    resident = st.radio("Have you been in the US longer than 365 days?", ["Yes", "No"])
    if resident == "Yes":
        has_foreign = st.radio("Do you have foreign assets/entities/income?", ["Yes", "No"])
        if has_foreign == "Yes":
            result = "US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons"
        else:
            result = "US Individual Tax Services (4XXXX) - Form 1040"
    else:
        itin = st.radio("Do you already have an ITIN?", ["Yes", "No"])
        if itin == "Yes":
            result = "NRA Individual Tax Services (4XXXX) - Form 1040NR"
        else:
            result = "NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on"
    st.session_state["client_result"] = result
    st.success(f"📄 {result}")
    show_done = True

# ------------------------
# Other Flow (Trust)
# ------------------------
elif filing_type == "Other":
    st.markdown("### 🧾 Trust Filing")
    trust_type = st.radio("Is it a Grantor or Non-Grantor trust?", ["Grantor", "Non-Grantor"])
    result = "Fiduciary or Trust (6XXXXX)"
    st.session_state["client_result"] = result
    st.success(f"📄 {result}")
    show_done = True

# ------------------------
# Done Button
# ------------------------
if show_done and st.button("✅ Done"):
    st.switch_page("pages/second.py")
