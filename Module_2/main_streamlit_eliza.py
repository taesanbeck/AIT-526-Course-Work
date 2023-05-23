import streamlit as st
from eliza_streamlit import reflect, analyze, talk_to_me

# THIS IS THE FRONT END FILE FOR THE STREAMLIT APP, NOT TO BE RUN ON ITS OWN

# Sources
# https://docs.streamlit.io/

# Make a title for the app
st.markdown("# Eliza app")

# Create a text input for the user to enter their statement
statement = st.text_input('Enter your statement:')

# If a statement is entered, analyze it and display the response
if statement:
    response = talk_to_me(statement)
    st.write('Eliza: ', response)

# Create a link to the GitHub Repo
st.markdown("[Link to GitHub Repository](https://github.com/taesanbeck/AIT-526-Course-Work/tree/main/Module_2)")

# Add everyones names
st.markdown("##### Contributors: Sean Lam, Henry Wu, George Cross, and Sid Beck")
