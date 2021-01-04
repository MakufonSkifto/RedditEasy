import requests
import json
import random
from .reddit import Reddit
from .exceptions import RequestError
import datetime
import requests.auth


class Subreddit:
    def __init__(self, subreddit, client_id, client_secret, user_agent):
        self.subreddit = subreddit
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

    def get_image(self):
        """
        :return: (str) The image URL of a random post
        """

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"User-Agent": self.user_agent}

        request = requests.get(f"https://www.reddit.com/r/{self.subreddit}/hot.json", headers=headers,
                               auth=client_auth)
        meme = json.loads(request.content)
        randompost = random.randint(0, meme["data"]["dist"] - 1)

        return meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]

    def get_post(self):
        """
        :return: (str) Info about the randomly selected post from the subreddit (hot)
        """

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"User-Agent": self.user_agent}

        request = requests.get(f"https://www.reddit.com/r/{self.subreddit}/hot.json", headers=headers,
                               auth=client_auth)
        meme = json.loads(request.content)

        try:

            try:
                randompost = random.randint(0, meme["data"]["dist"] - 1)
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
            except IndexError:
                randompost = 0
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

            pinned = meme["data"]["children"][randompost]["data"]["pinned"]
            stickied = meme["data"]["children"][randompost]["data"]["stickied"]
            spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
            s = meme["data"]["children"][randompost]["data"]["created"]
            media = meme["data"]["children"][randompost]["data"]["media"]
            updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

            try:
                flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
            except IndexError:
                flair_author = None
                flair_post = None

            nsfw = True if nsfw == "true" else False

            pinned = True if pinned == "true" else False

            stickied = True if stickied == "true" else False

            spoiler = True if spoiler == "true" else False

            if not media:
                contenttext = meme["data"]["children"][randompost]["data"]["selftext"]
                if contenttext == "":
                    contenttext = contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
            elif media:
                contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
            else:
                contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]

            return Reddit(
                content=contenttext,
                title=meme["data"]["children"][randompost]["data"]["title"],
                upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                score=meme["data"]["children"][randompost]["data"]["score"],
                downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                nsfw=nsfw,
                pinned=pinned,
                created_at=updated,
                author=meme["data"]["children"][randompost]["data"]["author"],
                post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                stickied=stickied,
                spoiler=spoiler,
                author_flair=flair_author,
                post_flair=flair_post,
                subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
            )
        except KeyError:
            try:

                try:
                    randompost = random.randint(0, meme["data"]["dist"] - 1)
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
                except IndexError:
                    randompost = 0
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

                pinned = meme["data"]["children"][randompost]["data"]["pinned"]
                stickied = meme["data"]["children"][randompost]["data"]["stickied"]
                spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
                media = meme["data"]["children"][randompost]["data"]["media"]
                s = meme["data"]["children"][randompost]["data"]["created"]

                try:
                    flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                    flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
                except IndexError:
                    flair_author = None
                    flair_post = None

                updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

                nsfw = True if nsfw == "true" else False

                pinned = True if pinned == "true" else False

                stickied = True if stickied == "true" else False

                spoiler = True if spoiler == "true" else False

                if not media:
                    contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
                    if contenttext == "":
                        contenttext = meme["data"]["children"][randompost]["data"]["url"]
                elif media:
                    contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
                else:
                    contenttext = meme["data"]["children"][randompost]["data"]["url"]

                return Reddit(
                    content=contenttext,
                    title=meme["data"]["children"][randompost]["data"]["title"],
                    upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                    total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                    score=meme["data"]["children"][randompost]["data"]["score"],
                    downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                    nsfw=nsfw,
                    pinned=pinned,
                    created_at=updated,
                    author=meme["data"]["children"][randompost]["data"]["author"],
                    post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                    stickied=stickied,
                    spoiler=spoiler,
                    author_flair=flair_author,
                    post_flair=flair_post,
                    subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
                )
            except KeyError:
                raise RequestError(meme["message"])

    def get_top_post(self):
        """
        :return: (str) Info about the randomly selected post (This will return the TOP POST OF TODAY, not the top post
         of all time)
        """

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"User-Agent": self.user_agent}

        request = requests.get(f"https://www.reddit.com/r/{self.subreddit}/top.json", headers=headers,
                               auth=client_auth)
        meme = json.loads(request.content)
        try:

            try:
                randompost = random.randint(0, meme["data"]["dist"] - 1)
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
            except IndexError:
                randompost = 0
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

            pinned = meme["data"]["children"][randompost]["data"]["pinned"]
            stickied = meme["data"]["children"][randompost]["data"]["stickied"]
            spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
            s = meme["data"]["children"][randompost]["data"]["created"]
            media = meme["data"]["children"][randompost]["data"]["media"]
            updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

            try:
                flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
            except IndexError:
                flair_author = None
                flair_post = None

            nsfw = True if nsfw == "true" else False

            pinned = True if pinned == "true" else False

            stickied = True if stickied == "true" else False

            spoiler = True if spoiler == "true" else False

            if not media:
                contenttext = meme["data"]["children"][randompost]["data"]["selftext"]
                if contenttext == "":
                    contenttext = contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
            elif media:
                contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
            else:
                contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]

            return Reddit(
                content=contenttext,
                title=meme["data"]["children"][randompost]["data"]["title"],
                upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                score=meme["data"]["children"][randompost]["data"]["score"],
                downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                nsfw=nsfw,
                pinned=pinned,
                created_at=updated,
                author=meme["data"]["children"][randompost]["data"]["author"],
                post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                stickied=stickied,
                spoiler=spoiler,
                author_flair=flair_author,
                post_flair=flair_post,
                subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
            )
        except KeyError:
            try:

                try:
                    randompost = random.randint(0, meme["data"]["dist"] - 1)
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
                except IndexError:
                    randompost = 0
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

                pinned = meme["data"]["children"][randompost]["data"]["pinned"]
                stickied = meme["data"]["children"][randompost]["data"]["stickied"]
                spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
                media = meme["data"]["children"][randompost]["data"]["media"]
                s = meme["data"]["children"][randompost]["data"]["created"]

                try:
                    flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                    flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
                except IndexError:
                    flair_author = None
                    flair_post = None

                updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

                nsfw = True if nsfw == "true" else False

                pinned = True if pinned == "true" else False

                stickied = True if stickied == "true" else False

                spoiler = True if spoiler == "true" else False

                if not media:
                    contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
                    if contenttext == "":
                        contenttext = meme["data"]["children"][randompost]["data"]["url"]
                elif media:
                    contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
                else:
                    contenttext = meme["data"]["children"][randompost]["data"]["url"]

                return Reddit(
                    content=contenttext,
                    title=meme["data"]["children"][randompost]["data"]["title"],
                    upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                    total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                    score=meme["data"]["children"][randompost]["data"]["score"],
                    downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                    nsfw=nsfw,
                    pinned=pinned,
                    created_at=updated,
                    author=meme["data"]["children"][randompost]["data"]["author"],
                    post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                    stickied=stickied,
                    spoiler=spoiler,
                    author_flair=flair_author,
                    post_flair=flair_post,
                    subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
                )
            except KeyError:
                raise RequestError(meme["message"])

    def get_new_post(self):
        """
        :return: (str) Info about the randomly selected post (new)
        """

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"User-Agent": self.user_agent}

        request = requests.get(f"https://www.reddit.com/r/{self.subreddit}/new.json", headers=headers,
                               auth=client_auth)
        meme = json.loads(request.content)
        try:

            try:
                randompost = random.randint(0, meme["data"]["dist"] - 1)
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
            except IndexError:
                randompost = 0
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

            pinned = meme["data"]["children"][randompost]["data"]["pinned"]
            stickied = meme["data"]["children"][randompost]["data"]["stickied"]
            spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
            s = meme["data"]["children"][randompost]["data"]["created"]
            media = meme["data"]["children"][randompost]["data"]["media"]
            updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

            try:
                flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
            except IndexError:
                flair_author = None
                flair_post = None

            nsfw = True if nsfw == "true" else False

            pinned = True if pinned == "true" else False

            stickied = True if stickied == "true" else False

            spoiler = True if spoiler == "true" else False

            if not media:
                contenttext = meme["data"]["children"][randompost]["data"]["selftext"]
                if contenttext == "":
                    contenttext = contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
            elif media:
                contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
            else:
                contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]

            return Reddit(
                content=contenttext,
                title=meme["data"]["children"][randompost]["data"]["title"],
                upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                score=meme["data"]["children"][randompost]["data"]["score"],
                downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                nsfw=nsfw,
                pinned=pinned,
                created_at=updated,
                author=meme["data"]["children"][randompost]["data"]["author"],
                post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                stickied=stickied,
                spoiler=spoiler,
                author_flair=flair_author,
                post_flair=flair_post,
                subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
            )
        except KeyError:

            try:

                try:
                    randompost = random.randint(0, meme["data"]["dist"] - 1)
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
                except IndexError:
                    randompost = 0
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

                pinned = meme["data"]["children"][randompost]["data"]["pinned"]
                stickied = meme["data"]["children"][randompost]["data"]["stickied"]
                spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
                media = meme["data"]["children"][randompost]["data"]["media"]
                s = meme["data"]["children"][randompost]["data"]["created"]

                try:
                    flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                    flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
                except IndexError:
                    flair_author = None
                    flair_post = None

                updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

                nsfw = True if nsfw == "true" else False

                pinned = True if pinned == "true" else False

                stickied = True if stickied == "true" else False

                spoiler = True if spoiler == "true" else False

                if not media:
                    contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
                    if contenttext == "":
                        contenttext = meme["data"]["children"][randompost]["data"]["url"]
                elif media:
                    contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
                else:
                    contenttext = meme["data"]["children"][randompost]["data"]["url"]

                return Reddit(
                    content=contenttext,
                    title=meme["data"]["children"][randompost]["data"]["title"],
                    upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                    total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                    score=meme["data"]["children"][randompost]["data"]["score"],
                    downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                    nsfw=nsfw,
                    pinned=pinned,
                    created_at=updated,
                    author=meme["data"]["children"][randompost]["data"]["author"],
                    post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                    stickied=stickied,
                    spoiler=spoiler,
                    author_flair=flair_author,
                    post_flair=flair_post,
                    subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
                )
            except KeyError:
                raise RequestError(meme["message"])

    def get_controversial_post(self):
        """
        :return: (str) Info about the randomly selected post (new)
        """

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"User-Agent": self.user_agent}

        request = requests.get(f"https://www.reddit.com/r/{self.subreddit}/controversial.json", headers=headers,
                               auth=client_auth)
        meme = json.loads(request.content)
        try:

            try:
                randompost = random.randint(0, meme["data"]["dist"] - 1)
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
            except IndexError:
                randompost = 0
                nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

            pinned = meme["data"]["children"][randompost]["data"]["pinned"]
            stickied = meme["data"]["children"][randompost]["data"]["stickied"]
            spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
            s = meme["data"]["children"][randompost]["data"]["created"]
            media = meme["data"]["children"][randompost]["data"]["media"]
            updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

            try:
                flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
            except IndexError:
                flair_author = None
                flair_post = None

            nsfw = True if nsfw == "true" else False

            pinned = True if pinned == "true" else False

            stickied = True if stickied == "true" else False

            spoiler = True if spoiler == "true" else False

            if not media:
                contenttext = meme["data"]["children"][randompost]["data"]["selftext"]
                if contenttext == "":
                    contenttext = contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
            elif media:
                contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
            else:
                contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]

            return Reddit(
                content=contenttext,
                title=meme["data"]["children"][randompost]["data"]["title"],
                upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                score=meme["data"]["children"][randompost]["data"]["score"],
                downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                nsfw=nsfw,
                pinned=pinned,
                created_at=updated,
                author=meme["data"]["children"][randompost]["data"]["author"],
                post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                stickied=stickied,
                spoiler=spoiler,
                author_flair=flair_author,
                post_flair=flair_post,
                subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
            )
        except KeyError:
            try:

                try:
                    randompost = random.randint(0, meme["data"]["dist"] - 1)
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]
                except IndexError:
                    randompost = 0
                    nsfw = meme["data"]["children"][randompost]["data"]["over_18"]

                pinned = meme["data"]["children"][randompost]["data"]["pinned"]
                stickied = meme["data"]["children"][randompost]["data"]["stickied"]
                spoiler = meme["data"]["children"][randompost]["data"]["spoiler"]
                media = meme["data"]["children"][randompost]["data"]["media"]
                s = meme["data"]["children"][randompost]["data"]["created"]

                try:
                    flair_author = meme["data"]["children"][randompost]["data"]["author_flair_text"]
                    flair_post = meme["data"]["children"][randompost]["data"]["link_flair_text"]
                except IndexError:
                    flair_author = None
                    flair_post = None

                updated = datetime.datetime.fromtimestamp(s).strftime("%d-%m-%Y %I:%M:%S UTC")

                nsfw = True if nsfw == "true" else False

                pinned = True if pinned == "true" else False

                stickied = True if stickied == "true" else False

                spoiler = True if spoiler == "true" else False

                if not media:
                    contenttext = meme["data"]["children"][randompost]["data"]["url_overridden_by_dest"]
                    if contenttext == "":
                        contenttext = meme["data"]["children"][randompost]["data"]["url"]
                elif media:
                    contenttext = meme["data"]["children"][randompost]["data"]["media"]["oembed"]["thumbnail_url"]
                else:
                    contenttext = meme["data"]["children"][randompost]["data"]["url"]

                return Reddit(
                    content=contenttext,
                    title=meme["data"]["children"][randompost]["data"]["title"],
                    upvote_ratio=meme["data"]["children"][randompost]["data"]["upvote_ratio"],
                    total_awards=meme["data"]["children"][randompost]["data"]["total_awards_received"],
                    score=meme["data"]["children"][randompost]["data"]["score"],
                    downvotes=meme["data"]["children"][randompost]["data"]["downs"],
                    nsfw=nsfw,
                    pinned=pinned,
                    created_at=updated,
                    author=meme["data"]["children"][randompost]["data"]["author"],
                    post_url=f"https://reddit.com{meme['data']['children'][randompost]['data']['permalink']}",
                    stickied=stickied,
                    spoiler=spoiler,
                    author_flair=flair_author,
                    post_flair=flair_post,
                    subreddit_subscribers=meme["data"]["children"][randompost]["data"]["subreddit_subscribers"]
                )
            except KeyError:
                raise RequestError(meme["message"])
