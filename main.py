import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="Contract Risk Checker", layout="wide")

st.title("📝 Contract Risk Checker (Demo)")
st.write("Upload a contract PDF and this demo will highlight **potentially risky clauses** using simple keyword spotting. "
         "No API keys required. (For real AI analysis, you can later plug in OpenAI or another LLM.)")

# Keywords we’ll scan for (very basic demo rules)
RISK_KEYWORDS = {
    "indemnity": "High risk — You may be liable for damages beyond your control.",
    "termination": "Medium risk — Check termination notice periods and conditions.",
    "liability": "High risk — Look for unlimited or vague liability terms.",
    "penalty": "High risk — Could impose heavy costs if breached.",
    "auto-renewal": "Medium risk — May renew without notice.",
    "jurisdiction": "Medium risk — Court location may not be favorable.",
    "intellectual property": "High risk — Could assign away your rights.",
    "confidentiality": "Medium risk — Weak terms may not protect you properly."
}

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

uploaded = st.file_uploader("Upload contract (PDF)", type=["pdf"])

if uploaded:
    st.success("File uploaded. Extracting text...")
    text = extract_text_from_pdf(uploaded)

    st.subheader("Extracted Contract Text (preview)")
    st.text_area("Contract text:", text[:2000] + ("..." if len(text) > 2000 else ""), height=200)

    st.subheader("Risk Analysis")
    risks_found = []
    for keyword, explanation in RISK_KEYWORDS.items():
        if keyword.lower() in text.lower():
            risks_found.append((keyword, explanation))

    if risks_found:
        for kw, expl in risks_found:
            st.warning(f"⚠️ Clause detected: **{kw.capitalize()}**\n\n{expl}")
    else:
        st.info("No risky clauses detected by simple keyword scan. (This is just a basic demo.)")

    st.markdown("---")
    st.caption("Note: This is a keyword-based demo. For real contract analysis, integrate with an AI model (requires API key).")

