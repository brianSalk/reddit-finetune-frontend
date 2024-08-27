import praw
import sys
import argparse
import os
import streamlit as st
import re
# Create Reddit instance using environment variables
reddit = praw.Reddit(
    client_secret=st.secrets['REDDIT_CLIENT_SECRET'],
    client_id=st.secrets['REDDIT_CLIENT_ID'],
    usename=st.secrets['REDDIT_USER_NAME'],
    password=st.secrets['REDDIT_PASSWORD'],
    user_agent='userboboozerforHooozzer'
)


def create(subreddits,comments,submission_body,
        questions_only,min_completion_length, max_completion_length,
        max_submissions, min_rating_for_sub, min_rating_for_comment,
        max_lines,cre_pattern, pre_pattern ,
        PROMPT_END=r'\n\n###\n\n', COMP_END="###"):
    """
    takes in all the user specified options as arguments
    returns a valid JSONL file based on the users specifications
    """
    st.write(reddit.user.me())
    st.write('WROTE THAT')
    if questions_only:
        PROMPT_END = '?'
    comp_regex = re.compile(cre_pattern) if cre_pattern is not None else None
    ans = []
    line_count = 0
    for sub in subreddits.split(' '):
        if line_count == max_lines:
            return "\n".join(ans)
        next_sub = reddit.subreddit(sub)
        sub_count = 0
        try:
            reddit.subreddits.search_by_name(next_sub, exact=True)
        except Exception:
            st.write(f':red[SUBREDDIT {next_sub} NOT FOUND]')
            continue
        for submission in next_sub.top(limit=1_000):
            scraped_current = False
            if sub_count == max_submissions:
                break
            if line_count == max_lines:
                return "\n".join(ans)
            title = submission.title.strip()
            if not re.search(pre_pattern, title):
                continue
            selftext = submission.selftext.strip()

            if questions_only and not title.endswith('?'):
                continue

            if questions_only:
                title = title[:-1]
            title = title.replace('"', "'")
            title = title.replace("\\", '')
            selftext = selftext.replace('\n', ' ')
            selftext = selftext.replace('"', "'")
            selftext = selftext.replace("\\", '')
            # Generate JSON string using submission body
            if selftext and submission_body and submission and len(selftext) >= min_completion_length and len(selftext) <= max_completion_length \
                and submission.score >= min_rating_for_sub \
                and (comp_regex is None or re.search(comp_regex,selftext) is not None):
                prompt = f'"prompt": "{title}{PROMPT_END}",'
                completion = f'"completion": " {selftext}{COMP_END}"'
                string = '{' + prompt + completion + '}'
                ans.append(string)
                line_count+=1
                scraped_current = True
            # Generate JSON string for comments
            if comments:
                comment_count = 0
                for comment in submission.comments:
                    if line_count == max_lines:
                        return "\n".join(ans)
                    if comment_count >= comments:
                        break
                    try:
                        selftext = comment.body.strip()
                    except Exception:
                        continue
                    selftext = selftext.replace('\n', ' ')
                    selftext = selftext.replace('"', "'")
                    selftext = selftext.replace('\\', '')
                    prompt = f'"prompt": "{title}{PROMPT_END}",'
                    completion = f'"completion": " {selftext}{COMP_END}"'
                    string = '{' + prompt + completion + '}'
                    if len(selftext) <= max_completion_length and \
                    len(selftext) >= min_completion_length and comment.score >= min_rating_for_comment:
                        ans.append(string)
                        scraped_current = True
                        line_count+=1
                        comment_count += 1
            if scraped_current == True:
                sub_count+=1
    return "\n".join(ans)
