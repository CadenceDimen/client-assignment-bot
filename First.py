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

# Reset progress at start
if "progress" not in st.session_state:
    st.session_state["progress"] = 0

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

show_done = False
answered = 0

# ------------------------
# Company Flow
# ------------------------
if filing_type == "Company":
    answered += 1
    st.markdown("### 🏢 Company Filing")
    st.markdown('<p style="font-size:18px;"><b>What type of entity do you have?</b></p>', unsafe_allow_html=True)
    entity_type = st.selectbox("Entity Type", ["", "Inc. or Corp.", "LLC"], index=0, label_visibility="collapsed")

    if entity_type:
        answered += 1
        if entity_type == "Inc. or Corp.":
            st.markdown('<p style="font-size:18px;"><b>Is the ownership US or Foreign?</b></p>', unsafe_allow_html=True)
            ownership = st.radio("Ownership", ["US", "Foreign"], index=None, label_visibility="collapsed")
            if ownership:
                answered += 1
                if ownership == "US":
                    st.markdown('<p style="font-size:18px;"><b>Is it a C-Corp or S-Corp?</b></p>', unsafe_allow_html=True)
                    corp_type = st.radio("Corp Type", ["C-Corp", "S-Corp"], index=None, label_visibility="collapsed")
                    if corp_type:
                        answered += 1
                        if corp_type == "C-Corp":
                            result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
                        else:
                            result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
                else:
                    result = "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F"

        elif entity_type == "LLC":
            st.markdown('<p style="font-size:18px;"><b>How many owners are there?</b></p>', unsafe_allow_html=True)
            owners = st.radio("Number of Owners", ["1 Owner", "2+ Owners"], index=None, label_visibility="collapsed")
            if owners:
                answered += 1
                if owners == "1 Owner":
                    st.markdown('<p style="font-size:18px;"><b>Are you Foreign or U.S.?</b></p>', unsafe_allow_html=True)
                    residency = st.radio("Residency", ["Foreign", "U.S."], index=None, label_visibility="collapsed")
                    if residency:
                        answered += 1
                        if residency == "Foreign":
                            st.markdown('<p style="font-size:18px;"><b>Do you have operations in the U.S. or U.S.-based income?</b></p>', unsafe_allow_html=True)
                            has_us_income = st.radio("U.S. Income", ["Yes", "No"], index=None, label_visibility="collapsed")
                            if has_us_income:
                                answered += 1
                                if has_us_income == "No":
                                    result = "Disregarded Entity DRE5472 (3XXXXX) - Form 5472 / Pro Form 1120"
                                else:
                                    result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120 (5472 add-on)"
                        else:
                            st.markdown('<p style="font-size:18px;"><b>Did you elect to be treated as a C-Corp or S-Corp?</b></p>', unsafe_allow_html=True)
                            elected = st.radio("C/S Election", ["Yes", "No"], index=None, label_visibility="collapsed")
                            if elected:
                                answered += 1
                                if elected == "Yes":
                                    st.markdown('<p style="font-size:18px;"><b>Is it a C-Corp or S-Corp?</b></p>', unsafe_allow_html=True)
                                    corp_type = st.radio("Corp Type Again", ["C-Corp", "S-Corp"], index=None, label_visibility="collapsed")
                                    if corp_type:
                                        answered += 1
                                        if corp_type == "C-Corp":
                                            result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
                                        else:
                                            result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
                                else:
                                    result = "US Individual Tax Services (4XXXX) - Form 1040 (with schedule c add-on)"
                elif owners == "2+ Owners":
                    st.markdown('<p style="font-size:18px;"><b>Do you want to stay in a partnership or become a corporation?</b></p>', unsafe_allow_html=True)
                    structure = st.radio("LLC Structure", ["Stay as a Partnership", "Become a Corporation", "Unsure"], index=None, label_visibility="collapsed")
                    if structure:
                        answered += 1
                        if structure == "Stay as a Partnership":
                            st.markdown('<p style="font-size:18px;"><b>Are the owners US or Foreign?</b></p>', unsafe_allow_html=True)
                            owner_type = st.radio("Partnership Owner Type", ["US", "Foreign"], index=None, label_visibility="collapsed")
                            if owner_type:
                                answered += 1
                                if owner_type == "US":
                                    result = "U.S. Partnership with Tax Services (2XXXXX) - Form 1065"
                                else:
                                    result = "Foreign Partnership with Tax Services (2XXXXX) - Form 1065 (ADD ONS 8804 & 8805)"

                        elif structure == "Become a Corporation":
                            st.markdown('<p style="font-size:18px;"><b>Is the ownership US or Foreign?</b></p>', unsafe_allow_html=True)
                            corp_owner = st.radio("Corp Owner Type", ["US", "Foreign"], index=None, label_visibility="collapsed")
                            if corp_owner:
                                answered += 1
                                if corp_owner == "US":
                                    st.markdown('<p style="font-size:18px;"><b>Is it a C-Corp or S-Corp?</b></p>', unsafe_allow_html=True)
                                    corp_type = st.radio("Corp Type 2", ["C-Corp", "S-Corp"], index=None, label_visibility="collapsed")
                                    if corp_type:
                                        answered += 1
                                        if corp_type == "C-Corp":
                                            result = "U.S. Corporation with Tax Services (2XXXXX) - Form 1120"
                                        else:
                                            result = "U.S. S-Corporation with Tax Services (2XXXXX) - Form 1120-S"
                                else:
                                    result = "Foreign Corporation with Tax Services (2XXXXX) - Form 1120-F"
                        else:
                            result = "Consulting or One Time Project - NON-TAX (8XXXXX)"

        if 'result' in locals():
            st.session_state["client_result"] = result
            st.success(f"📄 {result}")
            show_done = True

# ------------------------
# Personal Flow
# ------------------------
elif filing_type == "Just Personal":
    answered += 1
    st.markdown("### 👤 Personal Filing")
    st.markdown('<p style="font-size:18px;"><b>Have you been in the US longer than 365 days?</b></p>', unsafe_allow_html=True)
    resident = st.radio("US Residency", ["Yes", "No"], index=None, label_visibility="collapsed")
    if resident:
        answered += 1
        if resident == "Yes":
            st.markdown('<p style="font-size:18px;"><b>Do you have foreign assets/entities/income?</b></p>', unsafe_allow_html=True)
            has_foreign = st.radio("Foreign Income", ["Yes", "No"], index=None, label_visibility="collapsed")
            if has_foreign:
                answered += 1
                if has_foreign == "Yes":
                    result = "US Individual Tax Services (4XXXX) - Form 1040 with foreign add-ons"
                else:
                    result = "US Individual Tax Services (4XXXX) - Form 1040"
        else:
            st.markdown('<p style="font-size:18px;"><b>Do you already have an ITIN?</b></p>', unsafe_allow_html=True)
            itin = st.radio("ITIN Status", ["Yes", "No"], index=None, label_visibility="collapsed")
            if itin:
                answered += 1
                if itin == "Yes":
                    result = "NRA Individual Tax Services (4XXXX) - Form 1040NR"
                else:
                    result = "NRA Individual Tax Services (4XXXX) - Form 1040NR with W7 add-on"
        if 'result' in locals():
            st.session_state["client_result"] = result
            st.success(f"📄 {result}")
            show_done = True

# ------------------------
# Other Flow (Trust)
# ------------------------
elif filing_type == "Other":
    answered += 1
    st.markdown("### 🇾 Trust Filing")
    st.markdown('<p style="font-size:18px;"><b>Is it a Grantor or Non-Grantor trust?</b></p>', unsafe_allow_html=True)
    trust_type = st.radio("Trust Type", ["Grantor", "Non-Grantor"], index=None, label_visibility="collapsed")
    if trust_type:
        answered += 1
        result = "Fiduciary or Trust (6XXXXX)"
        st.session_state["client_result"] = result
        st.success(f"📄 {result}")
        show_done = True

# ------------------------
# Progress Bar (max 60%)
# ------------------------
progress = min(answered * 10, 60)
st.session_state["progress"] = progress
st.progress(progress / 100.0, text=f"Progress: {progress}%")

# ------------------------
# Done and Reset Buttons
# ------------------------
col_done, col_reset = st.columns([1, 1])
if show_done:
    with col_done:
        if st.button("✅ Done"):
            st.switch_page("pages/second.py")
    with col_reset:
        if st.button("🔄 Reset Form"):
            st.session_state.clear()
            st.rerun()
