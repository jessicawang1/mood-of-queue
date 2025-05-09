# Mood of Ticket Queue

A tool to help Ops team agents to log the mood of the patient support ticket queue throughout the day and visualize the emotional trend over time using  **Streamlit** and **Google Sheets**.

## Features
- Mood logging from a dropdown emoji menu (Celebratory:`🎉`, Happy: `😊`, Neutral: `😐`, Sad: `😕`, Angry: `😠`)
- Optional short notes to record more information about the queue mood
- Filter mood trend by date range (default is current day)
- Visualize mood counts over time grouped by day or total aggregates
- Click on legend to filter by emoji/mood type 

---
## Getting Started
### Run on Streamlit Cloud
Click the link here [Mood of Ticket Queue](https://mood-of-ticket-queue.streamlit.app/)
No local setup is required. 

### Run Locally
#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mood-of-the-queue.git
cd mood-of-the-queue
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Set Up Google Sheets Integration
1. Go to the [Google Developers Console](https://console.developers.google.com/)
2. Create a new project and enable the **Google Sheets API**
3. Create a service account and download the `creds.json` key file
4. Share your target Google Sheet with timestamp, mood, and notes columns (e.g., `Mood Tracker`) with the service account email

Make sure `creds.json` is placed in the root folder (do not commit— put file name in `.gitignore`).

---

#### 4. Run the App
```bash
streamlit run app.py
```

---


#### File Structure
```
├── app.py               # Main Streamlit app
├── creds.json           # Your Google API key (not tracked in Git)
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

---

#### Tech Stack
- **Streamlit**
- **Pandas**
- **Plotly** 
- **Google Sheets API** (using gspread)

---

#### .gitignore Reminder
Make sure `.gitignore` includes:
```
creds.json
```

---

## Possible Next Steps
### Visualization add-ons:
- Add filter by time of day (e.g. morning, afternoon, evening) to visualize changes in mood trends throughout the day 
- Include weekly or monthly filters when more mood entries have been logged
- View by percentages in addition to mood counts
### Further Analysis:
- Assign ordinal values to emojis (e.g. `🎉`:5, `😊`:4, `😐`:3, `😕`:2, `😠`:1) to calculate average mood trends and other numeric metrics
- Analyze notes using NLP to identify ticket queue highlights and pain points
