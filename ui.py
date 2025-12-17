import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Agentic AI – B2B RFP Automation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0B1220;
    color: #E5E7EB;
}

.header-box {
    background: linear-gradient(90deg, #0A2A66, #2563EB);
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 14px 36px rgba(0,0,0,0.5);
}

.section-box {
    background: #111827;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #1F2937;
    box-shadow: 0 10px 26px rgba(0,0,0,0.4);
    margin-bottom: 26px;
}

.metric-card {
    background: #0F172A;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #1E293B;
    text-align: center;
}

.metric-card h2 {
    color: #38BDF8;
    margin: 0;
}

.small {
    color: #9CA3AF;
    font-size: 13px;
}

.badge-high {
    color: #22C55E;
    font-weight: bold;
}

.badge-medium {
    color: #FACC15;
    font-weight: bold;
}

.badge-low {
    color: #EF4444;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-box">
    <h1>⚡ Agentic AI – B2B RFP Automation Platform</h1>
    <p>Autonomous Sales, Technical & Pricing Agents for Real-Time Tender Evaluation</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- TENDER URL INPUT ----------------
st.markdown("## 📤 Tender PDF URL")

tender_url = st.text_input(
    "Paste Tender / RFP PDF URL",
    placeholder="http://127.0.0.1:9000/Lt_cable.pdf"
)

# ---------------- PROCESS ----------------
if tender_url:
    with st.spinner("🤖 Fetching tender & running Agentic AI pipeline..."):
        response = requests.post(
            "http://127.0.0.1:8000/evaluate-tender",
            params={"tender_url": tender_url},   # ✅ FIXED LINE
            timeout=180
        )

    if response.status_code != 200:
        st.error("❌ Backend error while processing RFP")
        st.code(response.text)
        st.stop()

    data = response.json()

    # ---------------- AGENT METRICS ----------------
    st.markdown("## 📊 Agentic AI Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>Sales Agent</h2>
            <p class="small">RFP Identified & Structured</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{len(data.get("technical_recommendations", []))}</h2>
            <p class="small">SKU Recommendations</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹ {data['pricing']['total_cost']:,}</h2>
            <p class="small">Estimated Total Cost</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- CONFIDENCE ----------------
    st.markdown("## 🔐 Bid Confidence")

    confidence = data.get("confidence", "LOW").upper()

    badge_class = {
        "HIGH": "badge-high",
        "MEDIUM": "badge-medium",
        "LOW": "badge-low"
    }.get(confidence, "badge-low")

    st.markdown(
        f"<h3 class='{badge_class}'>Confidence Level: {confidence}</h3>",
        unsafe_allow_html=True
    )

    # ---------------- SALES AGENT ----------------
    st.markdown("## 🧠 Sales Agent – RFP Understanding")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.json(data["rfp_summary"], expanded=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- TECHNICAL AGENT ----------------
    st.markdown("## 🛠 Technical Agent – SKU Matching")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    tech_df = pd.DataFrame(data["technical_recommendations"])
    tech_df.rename(columns={
        "sku": "Recommended SKU",
        "spec_match_percent": "Spec Match (%)"
    }, inplace=True)

    st.dataframe(tech_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- PDF DOWNLOAD ----------------
    st.markdown("## 📄 Auto-Generated Bid Quotation")

    pdf_path = data.get("quotation_pdf")

    if pdf_path:
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "⬇ Download Professional Bid Quotation (PDF)",
                pdf_file,
                file_name="Bid_Quotation.pdf",
                mime="application/pdf"
            )
