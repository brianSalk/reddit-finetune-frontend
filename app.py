import os
import sys
import streamlit as st
import re

import create_jsonl
max_submissions_per_sub = 1_000
max_lines = float('inf')
comment_count = 0
min_sub_upvote=0
min_comment_upvote=0
comp_regex= ""
prompt_regex = ""
prompt_end=r'\n\n###\n\n'
comp_end="###"

with st.sidebar:
    st.title('Use this app to create a JSONL file to use for fine-tuning with openai models')
    st.write('this app uses submission titles as prompts and the submission text and/or comments as completions')
    st.write('follow along with the instructions [here](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)')
    st.title("found a bug or want to improve this app?")
    st.write("submit a pull request or open an issue [here](https://github.com/brianSalk/reddit-finetune-frontend)")

st.title(":green[Create Jsonl From Reddit]")
subreddits = st.text_input('enter subreddits seperated by spaces')


submission_body = st.checkbox('include the submission body in your jsonl', value = True)
questions_only = st.checkbox('questions only (prompt ends with "?")')
if st.checkbox('include comments'):
    comment_count = st.number_input('maximum number of comments to scrape per submission',min_value = 1, step=1)
if st.checkbox('set minimum comment upvote limit'):
    min_comment_upvote = st.number_input('only scrape comments with this many upvotes', min_value=1,step=1)
if st.checkbox('set minimum submission upvote limit'):
    min_sub_upvote = st.number_input('only scrape submissions with with many upvotes', min_value=1, step=1)
if st.checkbox('set maximum lines'):
    max_lines = st.number_input('maximum number of promt/completion pairs', min_value=1, step=1)
if st.checkbox('set maximum number of submissions per subreddit'):
    max_submissions_per_sub = st.number_input('maximum number of submissions per subreddit', min_value=1,max_value=1_000, step=1)
if st.checkbox('filter with regular expression'):
    prompt_regex = st.text_input('only include prompts that include the following regex')
    comp_regex = st.text_input('only inlude completions that include the following regex')
    if prompt_regex == "":
        prompt_regex = ".*"
    if comp_regex == "":
        comp_regex = ".*"
if st.checkbox(r'use custom prompt end (default is **\n\n###\n\n**)',disabled = questions_only, help=r'Each prompt should end with a fixed separator to inform the model when the prompt ends and the completion begins. A simple separator which generally works well is `\n\n###\n\n`. The separator should not appear elsewhere in any prompt. [openAI](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)'):
    prompt_end = st.text_input("prompt end")
if st.checkbox(r'use custom completion end (default is **###**)', help='Each completion should end with a fixed stop sequence to inform the model when the completion ends. A stop sequence could be \n, `###`, or any other token that does not appear in any completion.\n[openAI](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)'):
    comp_end = st.text_input("completion end")
if st.button('get jsonl', disabled=(comment_count == 0 and not submission_body)):
    if len(subreddits) > 0:
        st.write(f'creating jsonl from the following subreddits: :green[{subreddits}]')
        st.write('**please be patient while I create your JSONL file**')
        max_completion_length = 200
        min_completion_length = 2
        jsonl_text = create_jsonl.create(subreddits, comment_count, submission_body, 
                questions_only,min_completion_length,max_completion_length,
                max_submissions_per_sub, min_sub_upvote,min_comment_upvote, 
                max_lines,comp_regex,prompt_regex, 
                prompt_end, comp_end)
        st.write('your jsonl is ready, copy the text below')
        st.code(jsonl_text)
    else:
        st.write(':red[you must specify at least one subreddit]')
if comment_count == 0 and not submission_body:
    st.write(':red[you must use submission body and/or comments]')

    

