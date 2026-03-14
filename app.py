import streamlit as st
import logic_modules as lm
import sheet_handler as sh
from datetime import datetime

# Page Config
st.set_page_config(page_title="Ruhani SEO Engine", layout="wide")

st.title("🎼 Ruhani SEO Engine v3.0")
st.subheader("YouTube Content Optimization for Ikjot Ruhani Records")

# Sidebar for API Keys
with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Gemini API Key", type="password")
    yt_key = st.text_input("YouTube API Key", type="password")
    sheet_name = st.text_input("Google Sheet Name", value="Ruhani_SEO_Data")

# Main Input
user_lyrics = st.text_area("Enter Lyrics or Song Title", height=200)

if st.button("Generate SEO Strategy"):
    if not gemini_key or not yt_key:
        st.error("Please enter API Keys in the sidebar!")
    elif not user_lyrics:
        st.warning("Please enter some lyrics or a title.")
    else:
        with st.spinner("Analyzing Market & Generating AI Content..."):
            # 1. Fetch Competitor Data
            comp_tags = lm.get_competitor_insights(yt_key, user_lyrics[:50])
            
            # 2. Get AI Response
            prompt = lm.get_seo_prompt("Devotional", user_lyrics, comp_tags)
            ai_result = lm.generate_ai_content(gemini_key, prompt)
            
            # 3. Display Results in Tabs
            st.success("Analysis Complete!")
            tab1, tab2 = st.tabs(["SEO Output", "Thumbnail & Insights"])
            
            with tab1:
                st.markdown(ai_result)
                if st.button("Save to Google Sheets"):
                    row = [str(datetime.now()), user_lyrics[:100], ai_result]
                    status = sh.push_to_sheet(sheet_name, row)
                    if status == True:
                        st.balloons()
                        st.success("Synced with Google Sheets!")
                    else:
                        st.error(status)
            
            with tab2:
                st.write("### Competitor Gaps Identified:")
                st.info(", ".join(comp_tags) if comp_tags else "No competitor tags found.")