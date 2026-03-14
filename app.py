import streamlit as st
import logic_modules as lm
from datetime import datetime

st.set_page_config(page_title="Ruhani SEO Engine", layout="wide")

st.title("🎼 Ruhani SEO Engine v4.0")
st.caption("Official SEO Tool for Ikjot Ruhani Records")

user_input = st.text_area("Enter Lyrics or Song Title", height=150, placeholder="यहाँ अपने लिरिक्स या टाइटल पेस्ट करें...")

if st.button("Generate Strategy"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    else:
        # Secrets fetch karein
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
            yt_key = st.secrets["YOUTUBE_API_KEY"]
        except Exception as e:
            st.error(f"Secrets not found! Error: {e}")
            st.stop()

        with st.spinner("Analyzing Market & Creating Content..."):
            try:
                # Logic Execution
                comp_tags = lm.get_competitor_insights(yt_key, user_input[:50])
                prompt = lm.get_seo_prompt("Devotional", user_input, comp_tags)
                ai_result = lm.generate_ai_content(gemini_key, prompt)
                
                if "AI Generation Error" in ai_result:
                    st.error(ai_result)
                else:
                    st.success("Strategy Generated Successfully!")
                    
                    # Layout
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("📋 Optimized Metadata")
                        st.info("नीचे दिए गए बॉक्स के ऊपर 'Copy' बटन पर क्लिक करके इसे कॉपी करें।")
                        # Code block automatically provides a Copy button in Streamlit
                        st.code(ai_result, language="markdown")
                    
                    with col2:
                        st.subheader("🖼️ YouTube Preview")
                        st.markdown(f"""
                        <div style="background-color:#000; padding:20px; border-radius:10px; border: 2px solid #FF0000; text-align:center;">
                            <h2 style="color:white; font-size:22px;">{user_input[:25].upper()}</h2>
                            <p style="color:#AAA;">Ikjot Ruhani Records</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write("---")
                        st.write("**Quick Tags (Copy Ready):**")
                        # Ek alag chota box sirf tags ke liye
                        tags_only = ai_result.split("TAGS:")[1].split("HASHTAGS:")[0].strip() if "TAGS:" in ai_result else "See above"
                        st.code(tags_only)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")