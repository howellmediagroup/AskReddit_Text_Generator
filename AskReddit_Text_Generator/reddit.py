# reddit.py

import praw
from praw.models import MoreComments
from datetime import datetime
import os
import json
from dotenv import load_dotenv, find_dotenv

# Locate the .env file and load it
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)
else:
    raise FileNotFoundError(".env file not found. Please ensure it is in the project root directory.")

# Load environment variables
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
SECRET_KEY = os.getenv('REDDIT_SECRET_KEY')
USERAGENT = os.getenv('REDDIT_USERAGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')

# Raise error if any of the required values are missing
if not CLIENT_ID or not SECRET_KEY or not USERAGENT:
    raise ValueError("Required environment variables are missing. Please check your .env file.")

# Initialize PRAW Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET_KEY,
                     user_agent=USERAGENT,
                     username=USERNAME,
                     password=PASSWORD)

def get_data_from_link(post_url, comment_limit=20, max_char=300, min_char=45):
    submission = reddit.submission(url=post_url)
    
    # Prepare post data
    post_data = {
        'author': submission.author.name if submission.author else None,
        'subreddit': submission.subreddit.display_name,
        'upvotes': abbreviate_number(submission.ups),
        'comments_count': abbreviate_number(submission.num_comments),
        'content': submission.title,
        'name': submission.name,
        'comments': []
    }
    
    # Fetch top comments
    submission.comment_sort = 'top'
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()
    
    for comment in comments:
        if len(post_data['comments']) >= comment_limit:
            break
        if isinstance(comment, MoreComments):
            continue
        if min_char <= len(comment.body) <= max_char:
            comment_data = {
                'author': comment.author.name if comment.author else '[deleted]',
                'upvotes': abbreviate_number(comment.score),
                'content': comment.body,
            }
            post_data['comments'].append(comment_data)

    return post_data

def abbreviate_number(n):
    if n >= 1_000_000:
        return f"{n // 1_000_000}M" if n % 1_000_000 < 100_000 else f"{round(n / 1_000_000)}M"
    elif n >= 1_000:
        return f"{round(n / 1_000, 1)}K"
    else:
        return str(n)
