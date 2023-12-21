# import streamlit as st
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from google.auth.transport import requests
# import os

# # Set up your Google Client ID and Secret
# GOOGLE_CLIENT_ID = "<YOUR_GOOGLE_CLIENT_ID>"
# GOOGLE_CLIENT_SECRET = "<YOUR_GOOGLE_CLIENT_SECRET>"
# REDIRECT_URI = "<YOUR_REDIRECT_URI>"

# # Create a Flow instance
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for development!
# flow = Flow.from_client_secrets_file(
#     # client_secrets_file='client_secret.json',
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
#     redirect_uri=REDIRECT_URI
# )

# # Streamlit App
# def main():
#     st.title("Google Login with Streamlit")

#     # Session state to store user info
#     if "auth_token" not in st.session_state:
#         st.session_state["auth_token"] = None

#     # If not logged in
#     if st.session_state["auth_token"] is None:
#         # Generate a Google authentication link
#         auth_url, _ = flow.authorization_url(prompt='consent')
        
#         st.markdown(f"Please login using this [link]({auth_url}).")

#         # Input for authorization code
#         auth_code = st.text_input("Enter the authorization code:")
#         if auth_code:
#             try:
#                 flow.fetch_token(code=auth_code)
#                 idinfo = id_token.verify_oauth2_token(
#                     flow.credentials.id_token,
#                     requests.Request(),
#                     GOOGLE_CLIENT_ID
#                 )

#                 # Store the user info in session
#                 st.session_state["auth_token"] = idinfo
#                 st.success("Login successful!")
#             except Exception as e:
#                 st.error("Login failed: " + str(e))

#     # Display user info
#     if st.session_state["auth_token"]:
#         user_info = st.session_state["auth_token"]
#         st.write("Welcome, ", user_info.get("name"))
#         st.write("Email: ", user_info.get("email"))

# if __name__ == "__main__":
#     main()
