import streamlit as st
import create_jsonl
comment_count = 0
st.title("Create Jsonl From Reddit")
subreddits = st.text_input('enter subreddits seperated by spaces')

submission_body = st.checkbox('include the submission body in your jsonl')
questions_only = st.checkbox('questions only')
if st.checkbox('include comments'):
    comment_count = st.number_input('number of comments to scrape', step=1)
if st.button('get jsonl'):
    st.write(f'creating jsonl from the following subreddits: {subreddits}\n this may take some time')
    max_completion_length = 200
    min_completion_length = 2
    jsonl_text = create_jsonl.create(subreddits, comment_count, submission_body, questions_only,min_completion_length,max_completion_length)
    st.write('your jsonl is ready, copy the text below')
    st.code(jsonl_text)

    

