import praw
import sys
import argparse
import os

# Create Reddit instance
reddit = praw.Reddit(
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    client_id=os.environ['REDDIT_CLIENT_ID'],
    usename=os.environ['REDDIT_USER_NAME'],
    password=os.environ['REDDIT_PASSWORD'],
    user_agent='userboboozerforHooozzer'
)

# Set up argparse

def create(subreddits,comments=0,questions_only=True):
    # Constants
    PROMPT_END = '\n\n###\n\n'
    COMP_END = '.#,'
    if questions_only:
        PROMPT_END = '?'

    ans = []
    # Loop through subreddits and submissions
    for sub in subreddits.split(' '):
        next_sub = reddit.subreddit(sub)
        for submission in next_sub.top(limit=1000):
            title = submission.title.strip()
            selftext = submission.selftext.strip()

            # Skip if title does not end with question mark
            if questions_only and not title.endswith('?'):
                continue

            # Remove question mark from title
            if questions_only:
                title = title[:-1]

            # Replace special characters
            title = title.replace('"', "'")
            title = title.replace("\\", '')
            selftext = selftext.replace('\n', ' ')
            selftext = selftext.replace('"', "'")
            selftext = selftext.replace("\\", '')

            # Generate JSON string
            if selftext:
                prompt = f'"prompt": "{title}{PROMPT_END}",'
                completion = f'"completion": " {selftext}{COMP_END}"'
                string = '{' + prompt + completion + '}'
                ans.append(string)
            # Generate JSON string for comments
            if comments:
                comment_count = 0
                for comment in submission.comments:
                    if comment_count > comments:
                        break
                    try:
                        selftext = comment.body.strip()
                    except Exception:
                        break
                    selftext = selftext.replace('\n', ' ')
                    selftext = selftext.replace('"', "'")
                    selftext = selftext.replace('\\', '')
                    prompt = f'"prompt": "{title}{PROMPT_END}",'
                    completion = f'"completion": " {selftext}{COMP_END}"'
                    string = '{' + prompt + completion + '}'
                    ans.append(string)
                    comment_count += 1
    return "\n".join(ans)
