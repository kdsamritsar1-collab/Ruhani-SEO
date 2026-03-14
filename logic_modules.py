import google.generativeai as genai
from googleapiclient.discovery import build

def get_competitor_insights(api_key, query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        search = youtube.search().list(q=query, part='snippet', maxResults=3, type='video').execute()
        all_tags = []
        for item in search['items']:
            v_id = item['id']['videoId']
            details = youtube.videos().list(id=v_id, part='snippet').execute()
            all_tags.extend(details['items'][0]['snippet'].get('tags', []))
        return list(set(all_tags))[:15]
    except:
        return []

def get_seo_prompt(content_type, input_data, competitor_data):
    return f"""
    Act as a YouTube SEO Expert for '{content_type}' Music.
    Input: {input_data}
    Competitor Tags: {competitor_data}
    
    TASKS (English Output):
    1. TITLES: Suggest 1 SEO Title & 1 Emotional Title.
    2. DESCRIPTION: Write 3 paragraphs naturally fitting keywords.
    3. COMPETITOR GAP: 5 unique keywords missed by competitors.
    4. TAGS & HASHTAGS: 15 of each (comma separated).
    5. THUMBNAIL IDEA: Describe the scene, hero text, and colors.
    """

def generate_ai_content(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text