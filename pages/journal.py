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

# Reset form flag
reset = st.session_state.get('reset', False)

# User input for new journal entry
with st.form("new_entry", clear_on_submit=True):
    entry_date = st.date_input("Date", datetime.date.today())
    entry_text = st.text_area("Journal Entry", help="You can use Markdown formatting here.", key='entry_text')
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        new_entry = pd.DataFrame({'Date': [entry_date], 'Entry': [entry_text]})
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        st.session_state['reset'] = True

if reset:
    st.session_state['entry_text'] = ''
    st.session_state['reset'] = False

# Edit and Delete functionality
selected_entry_index = st.selectbox("Select an entry to edit or delete", data.index, format_func=lambda x: data.iloc[x]['Date'])
if st.button("Delete Entry"):
    data = data.drop(selected_entry_index)
    save_data(data)

with st.form("edit_entry"):
    edit_date = st.date_input("Edit Date", value=pd.to_datetime(data.iloc[selected_entry_index]['Date']))
    edit_text = st.text_area("Edit Journal Entry", value=data.iloc[selected_entry_index]['Entry'])
    edit_submit = st.form_submit_button("Save Changes")

    if edit_submit:
        data.at[selected_entry_index, 'Date'] = edit_date
        data.at[selected_entry_index, 'Entry'] = edit_text
        save_data(data)

# Display past entries
st.write("## Past Entries")
for _, row in data.iterrows():
    st.write(f"### {row['Date']}")
    st.markdown(row['Entry'], unsafe_allow_html=True)
    st.markdown("---")

# Run the app: streamlit run your_script.py
