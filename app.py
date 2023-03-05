import streamlit as st
#import create_jsonl
subreddits = st.text_input('enter subreddits seperated by spaces')
if st.button('get jsonl'):
    st.write(f'creating jsonl from subreddits: {subreddits}, this may take some time')
    st.text(create_jsonl.create(subreddits))

