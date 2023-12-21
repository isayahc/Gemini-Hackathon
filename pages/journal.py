import streamlit as st
import pandas as pd
from api_utils import get_entries, add_entry
from datetime import datetime
import json
import os

# Function to load and sort data
# def load_data():
#     try:
#         df = pd.read_csv('journal_entries.csv', parse_dates=['date'])
#         df.sort_values('date', ascending=False, inplace=True)
#         return df
#     except FileNotFoundError:
#         return pd.DataFrame(columns=['date', 'content'])
if os.getenv('DEV_ENV'):
    user_api_key= os.getenv('DEV_EMAIL')
    user_email = os.getenv('DEV_API_KEY')

def journal_page():

        def load_data():
            # try:
            #     user_email = st.session_state['user_email']
            #     user_api_key = st.session_state['user_api_key']
            # except KeyError:
            #     st.error("Please enter your email and API key in the sidebar.")
            #     # return pd.DataFrame(columns=['date', 'content'])
            # try:
            #     data = get_entries(email=user_email, api_key=user_api_key)
            #     df = pd.DataFrame(data)
            #     df['date'] = pd.to_datetime(df['date'])
            # except FileNotFoundError:
            #     df = pd.DataFrame(columns=['date', 'content'])
            # finally:
            #     return df
            user_email = st.session_state['user_email']
            user_api_key = st.session_state['user_api_key']
            data = get_entries(email=user_email, api_key=user_api_key)
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df

        # Function to save data
        def save_data(dataframe):
            dataframe.to_csv('journal_entries.csv', index=False)

        # Initialize Streamlit app
        st.title('My Journal')

        # Load and sort existing data
        data = load_data()
        # df['date'] = pd.to_datetime(df['date'])

        # for entry in data:
        #     entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d")

        # Form for new journal entry
        with st.form("new_entry", clear_on_submit=True):
            entry_date = st.date_input("date", pd.to_datetime('today').date())
            entry_text = st.text_area("Journal content", help="You can use Markdown formatting here.")
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # if isinstance(entry_date, datetime.date):
                entry_date = entry_date.isoformat()
                add_entry(email=user_email, api_key=user_api_key, date=entry_date, content=entry_text)
                # new_entry = pd.DataFrame({'date': [pd.to_datetime(entry_date)], 'content': [entry_text]})
                # data = pd.concat([data, new_entry], ignore_index=True)
                # data.sort_values('date', ascending=False, inplace=True)
                # save_data(data)
                st.experimental_rerun()

        # Display past entries with edit/delete options
        st.write("## Past Entries")
        for index, row in data.iterrows():
            cols = st.columns([0.8, 0.1, 0.1])
            with cols[0]:
                st.markdown(f"### {row['date'].strftime('%Y-%m-%d')}")
                st.markdown(row['content'], unsafe_allow_html=True)

            if cols[1].button("Edit", key=f"edit{index}"):
                st.session_state['edit_index'] = index
                st.session_state['edit_date'] = row['date'].date()
                st.session_state['edit_entry'] = row['content']

            if cols[2].button("Delete", key=f"del{index}"):
                data = data.drop(index).reset_index(drop=True)
                save_data(data)
                st.experimental_rerun()

        # Edit entry
        if 'edit_index' in st.session_state:
            with st.form("edit_entry"):
                edit_date = st.date_input("Edit date", value=st.session_state['edit_date'])
                edit_text = st.text_area("Edit Journal content", value=st.session_state['edit_entry'])
                save_edit = st.form_submit_button("Save Changes")

                if save_edit:
                    data.at[st.session_state['edit_index'], 'date'] = pd.to_datetime(edit_date)
                    data.at[st.session_state['edit_index'], 'content'] = edit_text
                    data.sort_values('date', ascending=False, inplace=True)
                    save_data(data)
                    del st.session_state['edit_index']
                    st.experimental_rerun()

        st.markdown("---")

        # Run the app: streamlit run your_script.py

if __name__ == "__main__":
    journal_page()
