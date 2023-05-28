import pandas as pd
import praw
from variables import *
import pandas as pd

class Reddit_API:
    
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id = REDDIT_CLIENT_ID,
            client_secret = REDDIT_CLIENT_SECRET,
            user_agent = REDDIT_USER_AGENT,
            username = REDDIT_USERNAME,
            password = REDDIT_PASSWORD
        )
        self.stocks = list(COMPANY_NAME_TO_TICKER.keys())
    
    def get_count_of_stock_mentions(self,desired_subreddit : str):
        '''
        Web scrapes Reddit for comments on the desiredSubreddit (Usually WallStreetBets). It then returns the stocks mentioned with counts as a dictionary.
        Parameters:
        reddit - Reddit connection from PRAW API
        desiredSubreddit - Name of the subreddit we want to scrape. For example, "wallstreetbets"
        Output:
        Dictionary with the keys being the name of companies we are interested in analyzing and the value pair being the number of times they are mentioned.
        '''
        stocksMentioned={}
        # comments=[]
        # Finding subreddit in Reddit, then finding posts, then finding comments. Add the comment count and stocks found to stocksMentioned dictionary.
        subreddit = self.reddit.subreddit(desired_subreddit)
        for submission in subreddit.hot(limit=REDDIT_POSTS_TO_SCAN):
            for comment in submission.comments:
                if hasattr(comment,"body"):
                    lowerComment=comment.body.lower()
                    for stock in self.stocks:
                        if stock in lowerComment:
                            if stock not in stocksMentioned:
                                stocksMentioned[stock]=1
                            else:
                                stocksMentioned[stock]+=1
                            # Uncomment this to have comment body appended. You must also return the comments list at the return statement.
                            #comments.append(comment.body)

        # Sort out confusion between Facebook changing name to Meta.
        # If both Meta and Facebook mentions found, then add them both to Meta.
        if "meta" in stocksMentioned and "facebook" in stocksMentioned:
            stocksMentioned["meta"] += stocksMentioned["facebook"]
            del stocksMentioned["facebook"]
        # If Facebook mention(s) are found but Meta mentions are not found, create "meta" key and copy FB mention count to it. Then Delete FB key.
        if "meta" not in stocksMentioned and "facebook" in stocksMentioned:
            stocksMentioned["meta"] = stocksMentioned["facebook"]
            del stocksMentioned["facebook"]

        return stocksMentioned#,comments