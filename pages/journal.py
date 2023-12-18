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

# Form for new journal entry
with st.form("new_entry", clear_on_submit=True):
    entry_date = st.date_input("Date", datetime.date.today())
    entry_text = st.text_area("Journal Entry", help="You can use Markdown formatting here.")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        new_entry = pd.DataFrame({'Date': [entry_date], 'Entry': [entry_text]})
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)

# Display past entries with edit/delete options
st.write("## Past Entries")
for index, row in data.iterrows():
    cols = st.columns([0.8, 0.1, 0.1])
    with cols[0]:
        st.markdown(f"### {row['Date']}")
        st.markdown(row['Entry'], unsafe_allow_html=True)

    if cols[1].button("Edit", key=f"edit{index}"):
        st.session_state['edit_index'] = index
        st.session_state['edit_date'] = row['Date']
        st.session_state['edit_entry'] = row['Entry']

    if cols[2].button("Delete", key=f"del{index}"):
        data = data.drop(index)
        save_data(data)
        st.experimental_rerun()

# Edit entry
if 'edit_index' in st.session_state:
    with st.form("edit_entry"):
        edit_date = st.date_input("Edit Date", value=pd.to_datetime(st.session_state['edit_date']))
        edit_text = st.text_area("Edit Journal Entry", value=st.session_state['edit_entry'])
        save_edit = st.form_submit_button("Save Changes")

        if save_edit:
            data.at[st.session_state['edit_index'], 'Date'] = edit_date
            data.at[st.session_state['edit_index'], 'Entry'] = edit_text
            save_data(data)
            del st.session_state['edit_index']  # Remove the index from the session state
            st.experimental_rerun()

st.markdown("---")

# Run the app: streamlit run your_script.py
