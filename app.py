import streamlit as st
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# Connect to Google Sheet with timestamp, mood, Note columns
@st.cache_resource
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Mood Tracker").sheet1
    return sheet

sheet = connect_to_gsheet()

# Initialize mood options and corresponding chart colors
moods = {
    "🎉": "Celebratory",
    "😊": "Happy",
    "😐": "Neutral",
    "😕": "Sad",
    "😠": "Angry"  
}
mood_colors = {
    '🎉': '#FFD700',
    '😊': '#32CD32',
    '😐': '#A9A9A9',
    '😕': '#1E90FF',
    '😠': '#FF6347'
}

st.title("Mood of Ticket Queue")
# Mood input form (dropdown emoji menu and optional short note)
st.header("Log a Mood")
with st.form("mood_form", clear_on_submit=True):
    emoji = st.selectbox("What is your current mood?", list(moods.keys()))  
    note = st.text_input("Optional: Add a short note (e.g. lots of Rx delays today)")
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Add logged timestamp, mood, and note to Google Sheet
        sheet.append_row([datetime.now().isoformat(), emoji, note])
        st.success("Mood successfully logged")
   
# Mood visualization
st.header("Visualize Mood Trends")
chart_title = "Mood Trend"
data = pd.DataFrame(sheet.get_all_records())
if not data.empty:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['date'] = data['timestamp'].dt.date
    today = datetime.today().date()
    # Select date range to display trend over time (default selection is today)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", today, max_value=today)
    with col2:
        end_date = st.date_input("End date", today, min_value=start_date, max_value=today)
    # Group by day option (changes data aggregation and title)
    group_by_day = st.checkbox("Group by day", value=False)
    if start_date and end_date and start_date <= end_date:
        range_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
        if not range_data.empty:
            if group_by_day:
                chart_title += " by Day"
                mood_trend = range_data.groupby(['date', 'mood']).size().reset_index(name='count')
                fig_range = px.bar(
                    mood_trend,
                    x='date',
                    y='count',
                    color='mood',
                    barmode='group',
                    labels={'date': 'Date', 'count': 'Count', 'mood': 'Mood'},
                    color_discrete_map=mood_colors
                )
                fig_range.update_layout(xaxis_tickformat="%B %-d, %Y")
            else:
                chart_title += " (Total)"
                mood_totals = range_data['mood'].value_counts().reset_index()
                mood_totals.columns = ['mood', 'count']
                fig_range = px.bar(
                    mood_totals,
                    x='mood',
                    y='count',
                    labels={'mood': 'Mood', 'count': 'Count'},
                    color='mood',
                    color_discrete_map=mood_colors
                )
            fig_range.update_layout(
                title={
                'text': chart_title,
                'font': {
                    'size': 25,
                    'color': '#222222'}
                }
            )
            st.plotly_chart(fig_range, use_container_width=True)
        else:
            st.info("No mood entries for this date range.")
else:
    st.info("No mood entries logged yet.")




