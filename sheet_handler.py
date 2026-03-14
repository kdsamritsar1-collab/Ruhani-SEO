import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def push_to_sheet(sheet_name, row_data):
    try:
        # Streamlit Secrets se credentials lena
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(row_data)
        return True
    except Exception as e:
        return f"Error: {e}"