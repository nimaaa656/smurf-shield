import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SMURF-Shield – AI Safety by SMASH SMURFS",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #6b0f1a; /* MAROON */
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        color: white !important;
    }

    textarea, input {
        background-color: #ffffff !important;
        color: black !important;
    }

    .stButton>button {
        background-color: #8b4513; /* BROWN */
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5em 1.5em;
    }

    .stButton>button:hover {
        background-color: #a0522d;
        color: white;
    }

    .stRadio label {
        color: white !important;
    }

    .stAlert {
        background-color: #8b1c2d !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.title("🛡️ SMURF-Shield")
st.subheader("AI-powered Deepfake & Impersonation Safety for Smart Cities")
st.caption("Built by **Team SMASH SMURFS 💙**")

# ---------------- NAVIGATION ----------------
page = st.radio(
    "Navigate",
    ["🏠 Home", "🔍 Check Content", "🛡️ What Should I Do?"]
)

# ---------------- LOGIC FUNCTIONS ----------------
def ai_generated_text_likelihood(text):
    t = text.lower()
    score = 0

    scam_pressure = [
        "urgent", "verify immediately", "do not ignore",
        "account will be frozen", "click here", "share this"
    ]

    legit_patterns = [
        "credited", "debited", "available balance",
        "transaction id", "ref no", "upi",
        "thank you for banking"
    ]

    for p in scam_pressure:
        if p in t:
            score += 2

    for p in legit_patterns:
        if p in t:
            score -= 2

    if t.count("!") >= 2:
        score += 1

    if score >= 4:
        return "🔴 High (Likely Synthetic / Scam-like)"
    elif score >= 2:
        return "🟡 Medium (Suspicious Patterns)"
    else:
        return "🟢 Low (Likely Genuine / Transactional)"


def ai_generated_video_likelihood(video_file):
    filename = video_file.name.lower()
    score = 0

    if any(x in filename for x in ["ai", "deepfake", "synthetic", "generated"]):
        score += 2

    if video_file.size < 5 * 1024 * 1024:
        score += 1

    if score >= 3:
        return "🔴 High (Likely AI-Generated)"
    elif score >= 1:
        return "🟡 Medium (Possibly AI-Generated)"
    else:
        return "🟢 Low (Likely Authentic)"


def impersonation_inconsistency_score(text):
    t = text.lower()
    score = 0

    if "neft" in t and "upi" in t:
        score += 2

    if "call" in t and ("bank" in t or "help" in t or "helpline" in t):
        score += 2

    weird_phrases = [
        "on by", "helps lines", "linked to vpa.",
        "credited to a/c", "upi ref no ("
    ]

    for p in weird_phrases:
        if p in t:
            score += 1

    if sum(c.isdigit() for c in t) > 25:
        score += 1

    return score

# ---------------- PAGES ----------------
if page == "🏠 Home":
    st.header("🚨 Why This Matters")
    st.write("""
    In smart cities, **deepfakes and impersonation scams** can cause:
    - Financial loss  
    - Public panic  
    - Loss of trust in digital systems  
    """)

    st.header("💡 Our Solution")
    st.write("""
    **SMURF-Shield** evaluates:
    - AI-generated likelihood  
    - Message intent  
    - Impersonation inconsistencies  
    - Risk to citizens  
    """)

    st.markdown("---")
    st.caption("Developed by **Team SMASH SMURFS**")

elif page == "🔍 Check Content":
    st.header("🔍 Check Suspicious Content")

    video = st.file_uploader(
        "Upload a suspicious video (optional)",
        type=["mp4", "mov", "avi"]
    )

    text = st.text_area(
        "Paste message / caption / transcript",
        placeholder="Example: URGENT bank alert. Verify immediately."
    )

    if st.button("ANALYSE"):
        if not text and not video:
            st.warning("Please upload a video or enter text.")
        else:
            st.subheader("🧠 Analysis Result")

            if video:
                st.video(video)
                st.write(
                    f"**Video AI-Generated Likelihood:** "
                    f"{ai_generated_video_likelihood(video)}"
                )
                st.info("Video analysis uses metadata & context only.")

            if text:
                t = text.lower()

                st.write(
                    f"**Text AI-Generated Likelihood:** "
                    f"{ai_generated_text_likelihood(text)}"
                )

                legit_transaction = any(
                    p in t for p in [
                        "credited", "debited", "available balance",
                        "transaction id", "ref no", "upi",
                        "thank you for banking"
                    ]
                )

                scam_signals = any(
                    p in t for p in [
                        "urgent", "verify immediately",
                        "account will be frozen",
                        "do not ignore", "click here"
                    ]
                )

                impersonation_score = impersonation_inconsistency_score(text)

                if legit_transaction and impersonation_score >= 3:
                    intent = "Bank Impersonation Scam"
                    risk = "🔴 High"
                elif legit_transaction and not scam_signals:
                    intent = "Benign / Transactional"
                    risk = "🟢 Low"
                elif scam_signals:
                    intent = "Financial Scam"
                    risk = "🔴 High"
                else:
                    intent = "Unclear / Needs Verification"
                    risk = "🟡 Medium"

                st.write(f"**Detected Intent:** {intent}")
                st.write(f"**Risk Level:** {risk}")

                if impersonation_score >= 3:
                    st.warning(
                        "This message imitates a legitimate bank alert "
                        "but contains inconsistencies typical of scams."
                    )

            st.subheader("📖 Explanation")
            st.write(
                "SMURF-Shield provides **likelihood-based assessment**, "
                "not absolute judgments."
            )

elif page == "🛡️ What Should I Do?":
    st.header("🛡️ Citizen Safety Guidance")

    st.markdown("""
    ### 🔴 High Risk
    - Do not respond or share  
    - Do not call numbers in the message  
    - Verify via official apps or websites  

    ### 🟡 Medium Risk
    - Be cautious  
    - Cross-check information  

    ### 🟢 Low Risk
    - Likely safe  
    - Still verify before acting  
    """)

    st.info(
        "SMURF-Shield is a decision-support system. "
        "Final judgment remains with humans."
    )
