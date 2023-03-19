import os
import sys
import streamlit as st

import create_jsonl

comment_count = 0
min_sub_upvote=0
min_comment_upvote=0
st.title("Create Jsonl From Reddit")
subreddits = st.text_input('enter subreddits seperated by spaces')

submission_body = st.checkbox('include the submission body in your jsonl')
questions_only = st.checkbox('questions only')
if st.checkbox('include comments'):
    comment_count = st.number_input('number of comments to scrape', step=1)
if st.checkbox('set minimum comment upvote limit'):
    min_comment_upvote = st.number_input('only scrape comments with this many upvotes', min_value=1,step=1)
if st.checkbox('set minimum submission upvote limit'):
    min_sub_upvote = st.number_input('only scrape submissions with with many upvotes', min_value=1, step=1)
if st.button('get jsonl'):
    st.write(f'creating jsonl from the following subreddits: {subreddits}\n this may take some time')
    max_completion_length = 200
    min_completion_length = 2
    jsonl_text = create_jsonl.create(subreddits, comment_count, submission_body, questions_only,min_completion_length,max_completion_length,1000, "feature not supported", min_sub_upvote,min_comment_upvote)
    st.write('your jsonl is ready, copy the text below')
    st.code(jsonl_text)

    

