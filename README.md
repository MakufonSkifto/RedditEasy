[![Documentation Status](https://readthedocs.org/projects/redditeasy/badge/?version=latest)](https://redditeasy.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/MakufonSkifto/redditeasy)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/MakufonSkifto/redditeasy)](https://github.com/ExpDev07/coronavirus-tracker-api/stargazers) 
[![PyPI version](https://badge.fury.io/py/redditeasy.svg)](https://badge.fury.io/py/redditeasy)
[![Monthly Downloads](https://img.shields.io/pypi/dm/redditeasy.svg)](https://badge.fury.io/py/redditeasy)
[![Downloads](https://pepy.tech/badge/redditeasy)](https://pepy.tech/project/redditeasy)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/22632d363d7747acbbcf357c5b6795c4)](https://www.codacy.com/gh/MakufonSkifto/RedditEasy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MakufonSkifto/RedditEasy&amp;utm_campaign=Badge_Grade)
[![Python Versions](https://img.shields.io/badge/Python-3%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)](https://img.shields.io/badge/Python-3%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue.svg)
# RedditEasy

RedditEasy is a rapidly-fast API wrapper for getting posts using the Reddit JSON API with both sync and async options

## Install
To install RedditEasy, do:

``pip install redditeasy`` 

OR

``python -m pip install redditeasy``

OR (not recommended)

``pip install git+https://github.com/MakufonSkifto/RedditEasy.git``

## Documentation
Docs can be found [here](https://redditeasy.readthedocs.io/en/latest/)

## Async RedditEasy
Yes, there is an async version of RedditEasy. To use it, you need to use the Async classes. Which are `AsyncSubreddit` and `AsyncUser`

Here is a small example on using `AsyncSubreddit`: https://github.com/MakufonSkifto/RedditEasy/blob/main/examples/async_meme.py

You can and should use this in a discord.py bot. The normal classes could cause a [blocking](https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean) in an async program.

This **will not** work outside an async function whatsoever.

## Usage

### Without Reddit API client info
This method is not suggested as it may be slow and throw errors more often

```python
import redditeasy
import datetime

# To get your Reddit API client info go to
# https://www.reddit.com/prefs/apps
# and create an app

# For more detailed explanation, see this image: https://i.imgur.com/Ri13AQu.png


post = redditeasy.Subreddit()

postoutput = post.get_post(subreddit="dankmemes") # Subreddit name

# Formatted version of created_at
formatted_time = datetime.datetime.fromtimestamp(postoutput.created_at).strftime("%d/%m/%Y %I:%M:%S UTC")

print(f"Posts Title: {postoutput.title}\n"
      f"Posts Content: {postoutput.content}\n"
      f"Posts Author: u/{postoutput.author}\n"
      f"Posts URL: {postoutput.post_url}\n"
      f"Spoiler?: {postoutput.spoiler}\n"
      f"Post Created At: {formatted_time}\n"
      f"Posts Upvote Count: {postoutput.score}\n"
      f"Posts Award Count: {postoutput.total_awards}\n"
      f"NSFW?: {postoutput.nsfw}\n"
      f"Post Flair: {postoutput.post_flair}\n"
      f"User Flair: {postoutput.author_flair}\n"
      f"Subreddit Subscribers: {postoutput.subreddit_subscribers}\n"
      f"Comment count: {postoutput.comment_count}\n"
      f"Is Media?: {postoutput.is_media}\n"
      f"Subreddit Name: r/{postoutput.subreddit_name}\n"
      f"Content Type: {postoutput.content_type}")

```

### With Reddit API client info

```python
import redditeasy
import datetime

# To get your Reddit API client info go to
# https://www.reddit.com/prefs/apps
# and create an app

# For more detailed explanation, see this image: https://i.imgur.com/Ri13AQu.png


post = redditeasy.Subreddit(client_id="",            # Your client ID
                            client_secret="",        # Your client secret
                            user_agent=""            # Your user agent (ex: ClientName/0.1 by YourUsername")
                            )

postoutput = post.get_post(subreddit="dankmemes")    # Subreddit name

# Formatted version of created_at
formatted_time = datetime.datetime.fromtimestamp(postoutput.created_at).strftime("%d/%m/%Y %I:%M:%S UTC")

print(f"Posts Title: {postoutput.title}\n"
      f"Posts Content: {postoutput.content}\n"
      f"Posts Author: u/{postoutput.author}\n"
      f"Posts URL: {postoutput.post_url}\n"
      f"Spoiler?: {postoutput.spoiler}\n"
      f"Post Created At: {formatted_time}\n"
      f"Posts Upvote Count: {postoutput.score}\n"
      f"Posts Award Count: {postoutput.total_awards}\n"
      f"NSFW?: {postoutput.nsfw}\n"
      f"Post Flair: {postoutput.post_flair}\n"
      f"User Flair: {postoutput.author_flair}\n"
      f"Subreddit Subscribers: {postoutput.subreddit_subscribers}\n"
      f"Comment count: {postoutput.comment_count}\n"
      f"Is Media?: {postoutput.is_media}\n"
      f"Subreddit Name: r/{postoutput.subreddit_name}\n"
      f"Content Type: {postoutput.content_type}")

```

More examples are in the [examples folder](https://github.com/MakufonSkifto/RedditEasy/tree/main/examples)

## Getting Reddit API client info
To get your Reddit API client info go to
https://www.reddit.com/prefs/apps
and create a script.

![](https://i.imgur.com/Ri13AQu.png)

(You don't have to fill "redirect_uri")

## Changelog

Changelog can be found [here](https://redditeasy.readthedocs.io/en/latest/changelog.html)

## Operating Systems

All of RedditEasy's versions were tested in `Windows`, `Linux (Ubuntu)` and `MacOS`

## Errors

The module will raise `redditeasy.exceptions.RequestError`  if there was an error with the request. Traceback will show the details about the error

The module will raise `redditeasy.exceptions.EmptyResult` if the given user / subreddit is empty

## Issues

If you have any issues with RedditEasy, please report them via the [issue tracker](https://github.com/MakufonSkifto/RedditEasy/issues)
