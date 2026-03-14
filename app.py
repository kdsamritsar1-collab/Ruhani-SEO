import streamlit as st
import logic_modules as lm
import sheet_handler as sh
from datetime import datetime

st.set_page_config(page_title="Ruhani SEO Engine", layout="wide")

st.title("🎼 Ruhani SEO Engine v3.5")
st.caption("Official SEO Tool for Ikjot Ruhani Records")

user_input = st.text_area("Enter Lyrics or Song Title", height=150, placeholder="यहाँ अपने लिरिक्स पेस्ट करें...")

if st.button("Generate Strategy"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    else:
        # Step 1: Initialize keys to None
        gemini_key = None
        yt_key = None
        sheet_name = None

        # Step 2: Try to fetch from secrets
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            yt_key = st.secrets["YOUTUBE_API_KEY"]
            sheet_name = st.secrets["SHEET_NAME"]
        except Exception as e:
            st.error(f"Secrets not found! Error: {e}")
            st.stop()

        # Step 3: Run Logic only if keys are present
        if gemini_key and yt_key:
            with st.spinner("Analyzing Market & Creating Content..."):
                try:
                    comp_tags = lm.get_competitor_insights(yt_key, user_input[:50])
                    prompt = lm.get_seo_prompt("Devotional", user_input, comp_tags)
                    ai_result = lm.generate_ai_content(gemini_key, prompt)
                    
                    if "AI Generation Error" in ai_result:
                        st.error(ai_result)
                    else:
                        st.success("Ready!")
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("### 📋 Optimized Metadata")
                            st.markdown(ai_result)
                            
                            # Session state use karein taaki button click par data ghum na ho
                            if st.button("🚀 Sync to Google Sheet"):
                                row = [str(datetime.now()), user_input[:100], ai_result]
                                status = sh.push_to_sheet(sheet_name, row)
                                if status == True:
                                    st.balloons()
                                    st.success("Data added to Google Sheets!")
                                else:
                                    st.error(f"Sync failed: {status}")
                        
                        with col2:
                            st.subheader("🖼️ YouTube Preview")
                            st.markdown(f"""
                            <div style="background-color:#000; padding:20px; border-radius:10px; border: 2px solid #FF0000; text-align:center;">
                                <h2 style="color:white; font-size:22px;">{user_input[:25].upper()}</h2>
                                <p style="color:#AAA;">Ikjot Ruhani Records</p>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An unexpected error occurred during processing: {e}")