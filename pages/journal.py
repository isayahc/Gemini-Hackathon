# Import necessary libraries
import streamlit as st
import datetime
import pandas as pd

# Function to load data
def load_data():
    try:
        return pd.read_csv('journal_entries.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Entry'])

# Function to save data
def save_data(dataframe):
    dataframe.to_csv('journal_entries.csv', index=False)

# Initialize Streamlit app
st.title('My Journal')

# Load existing data
data = load_data()

# User input for new journal entry
with st.form("new_entry"):
    entry_date = st.date_input("Date", datetime.date.today())
    entry_text = st.text_area("Journal Entry")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Add new entry to the data
        data = data.append({'Date': entry_date, 'Entry': entry_text}, ignore_index=True)
        save_data(data)

# Display past entries
st.write("## Past Entries")
for _, row in data.iterrows():
    st.write(f"### {row['Date']}")
    st.write(row['Entry'])
    st.markdown("---")

# Run the app: streamlit run your_script.py
