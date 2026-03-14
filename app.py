import streamlit as st
import logic_modules as lm
import sheet_handler as sh
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Ruhani SEO Engine", layout="wide")

# --- Header ---
st.title("🎼 Ruhani SEO Engine v3.5")
st.caption("Official SEO Tool for Ikjot Ruhani Records")

# --- Main Input ---
user_input = st.text_area("Enter Lyrics or Song Title", height=150, placeholder="यहाँ अपने लिरिक्स पेस्ट करें...")

# Button to trigger logic
if st.button("Generate Strategy"):
    # Check if input is empty
    if not user_input.strip():
        st.warning("Please enter some text first.")
        st.stop()

    # Automatic Secrets Fetching
    try:
        # Ye line sidebar ki jagah piche se keys uthayegi
        gemini_key = st.secrets["GEMINI_API_KEY"]
        yt_key = st.secrets["YOUTUBE_API_KEY"]
        sheet_name = st.secrets["SHEET_NAME"]
    except Exception as e:
        st.error(f"Secrets not found in Streamlit Cloud! Error: {e}")
        st.stop()

  # app.py mein badlav
with st.spinner("Analyzing Market & Creating Content..."):
    try:
        comp_tags = lm.get_competitor_insights(yt_key, user_input[:50])
        prompt = lm.get_seo_prompt("Devotional", user_input, comp_tags)
        ai_result = lm.generate_ai_content(gemini_key, prompt)
        
        if "AI Generation Error" in ai_result:
            st.error(ai_result)
        else:
            st.success("Ready!")
            # ... baaki code
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")