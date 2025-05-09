import streamlit as st
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# Google Sheets auth
@st.cache_resource
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mood Tracker").sheet1
    return sheet

sheet = connect_to_gsheet()

# Mood options
moods = {
    "😊": "Happy",
    "😠": "Angry",
    "😕": "Neutral"
}

# Mood input
st.title("Mood of the Queue")
emoji = st.selectbox("What is your mood?", list(moods.keys()))
note = st.text_input("Add a short note (optional)")
if st.button("Submit"):
    sheet.append_row([datetime.now().isoformat(), emoji, note])
    st.success("Mood successfully logged")

# Mood chart
st.header("Mood Chart")
data = pd.DataFrame(sheet.get_all_records())
if not data.empty:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    mood_counts = today['mood'].value_counts().reset_index()
    fig = px.bar(mood_counts, x='index', y='mood', labels={'index': 'Mood', 'mood': 'Count'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data logged yet.")