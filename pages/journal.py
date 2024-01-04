import streamlit as st
import pandas as pd
from src.Utils.api_utils import get_entries, add_entry, delete_entry, update_entry, query_entries
from datetime import datetime
import json
import os
from typing import Any, Dict, List, Optional, Union


if os.getenv('DEV_ENV'):
    user_api_key = os.getenv('DEV_API_KEY')
    user_email = os.getenv('DEV_EMAIL')
    st.session_state['user_email'] = user_email
    st.session_state['user_api_key'] = user_api_key
else:
    user_email = st.session_state['user_email']
    user_api_key = st.session_state['user_api_key']

def load_data():
    user_email = st.session_state['user_email']
    user_api_key = st.session_state['user_api_key']
    data = get_entries(email=user_email, api_key=user_api_key)

    if data:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

    else:
        df = pd.DataFrame(["id", "email", "date", "content"])
    return df

@st.cache_data(ttl=(3600/2))
def journal_rag():
    query = "based on the content of the data provide:\
        1: the user with some tips on their life style, \
        2: comment on progress they have made if any\
        ## additional notes:\
        please speak to the user directly"
    
    
        # please also take notice of the dates of the entries and determin if the user is progressing in anyway"
    data = query_entries(email=user_email, api_key=user_api_key, query=query)
    return data

@st.cache_data(ttl=(3600/2))
def search_for_food_insights():
    query = "based on the content of the data provide:\
        1: the user with some tips on their life style, \
        2: find any dietary needs\
        3: find any favorite foods\
        ## additional notes:\
        please speak to the user directly"
    
    
        # please also take notice of the dates of the entries and determin if the user is progressing in anyway"
    data = query_entries(email=user_email, api_key=user_api_key, query=query)
    
    x=0
    return data

def delete_entry_with_id(entry_id: str):
    delete_entry(email=user_email, api_key=user_api_key, entry_id=entry_id)
    st.session_state['data'] = load_data()  # Reload the data
    st.experimental_rerun()

# Function to save data
def save_data(dataframe):
    dataframe.to_csv('journal_entries.csv', index=False)


def journal_page():

    with st.spinner("Please wait..."):
        st.title('Your Personal Wellness')
        st.markdown("This is where you can your progress and thought with regards to health and wellness. All information you input will used to help me provide you with the best possible service. You can keep it open ended and i will use it to help you with your goals.")

        journal_rag_response:dict = journal_rag()
        food_insight:dict = search_for_food_insights()

        st.title("Your food insights")
        st.markdown(food_insight['response'])


        st.title("Life Progress")
        st.markdown(journal_rag_response['response'])
        data = load_data()
    st.success("communicating with server...")

    

    if 'editing_entry' not in st.session_state:
        st.session_state['editing_entry'] = None

    st.title("Input New Text Entry")
    with st.form("new_entry", clear_on_submit=True):
        # Get today's date as a date object
        today = pd.to_datetime('today').date()

        # Format today's date as a string in the 'YYYY-MM-DD' format
        formatted_today = today.strftime('%Y-%m-%d')


        entry_date = st.date_input("Date", today)

        
        entry_text = st.text_area("Journal content", help="You can use Markdown formatting here.")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            entry_date = entry_date.isoformat()

            add_entry(
                email=user_email,
                api_key=user_api_key,
                date=entry_date, 
                content=entry_text
                )

            st.experimental_rerun()

    if not data.empty and 'date' in data.columns:

        st.title("Your Journal Entries")
        for idx, row in data.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([5, 1, 1])
                with col1:
                    st.markdown(f"**{row['date'].strftime('%Y-%m-%d')}**")
                    if st.session_state['editing_entry'] == row['id']:
                        with st.form(key=f'form_{idx}'):
                            new_entry_date = st.date_input("Date", today)
                            new_entry_date = entry_date.isoformat()
                            new_content = st.text_area("Edit your entry:", value=row['content'])
                            save_button = st.form_submit_button('Save')
                            if save_button:
                                print((row['id'], new_content))
                                # update_entry_with_id(row['id'], new_content)
                                # dated = row['date'].strftime('%Y-%m-%d')
                                update_entry(email=user_email, api_key=user_api_key, entry_id=row['id'], date=new_entry_date, content=new_content)
                                st.session_state['editing_entry'] = None
                                st.experimental_rerun()
                    else:
                        st.markdown(row['content'])

                with col2:
                    if st.session_state['editing_entry'] != row['id']:
                        
                        edit_button = st.button('Edit', key=f'edit_{idx}')
                        if edit_button:
                            st.session_state['editing_entry'] = row['id']

                with col3:
                    delete_button = st.button('Delete', key=f'delete_{idx}')
                    if delete_button:
                        delete_entry_with_id(row['id'])
                        st.experimental_rerun()
    else:
         
        st.write("No data available")
        st.markdown("---")

if __name__ == "__main__":
    journal_page()
