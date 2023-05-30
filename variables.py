import datetime

# OpenAI Info
OPEN_AI_API_KEY = r''
# Define what kind of responses you want ChatGPT to produce. Who should this chat bot emulate?
OPEN_AI_CHARACTER = r''

# Website Info
WEBSITE_REPO_PATH = r""
TWITTER_PATH = WEBSITE_REPO_PATH + r""
SCRIPT_PATH = r''
GIT_BRANCH = r''

# Reddit Info
USER_AGENT=r""
REDDIT_CLIENT_ID=r""
REDDIT_CLIENT_SECRET=r""
REDDIT_USER_AGENT=r""
# Add username/password for a Reddit account.
REDDIT_USERNAME=r""
REDDIT_PASSWORD=r""

# Twitter Info
TWITTER_API_KEY=r""
TWITTER_API_SECRET=r""
TWITTER_BEARER_TOKEN=r""
TWITTER_CLIENT_ID=r""
TWITTER_CLIENT_SECRET=r""
TWITTER_ACCESS_TOKEN=r""
TWITTER_ACCESS_TOKEN_SECRET=r""
# Max number of tweets to pull for replying to mentions.
TWITTER_MAX_QUERY_RESULTS_FOR_MENTIONS = 100
# Not used anymore.
CALLBACKURL = r"oob"

REDDIT_POSTS_TO_SCAN = 100
DESIRED_SUBREDDIT = r"wallstreetbets"

# Seasonal data for the year 2000. (Leap year)
START_OF_YEAR = datetime.date(2000,1,1)
END_OF_YEAR = datetime.date(2000,12,31)

START_OF_WINTER = datetime.date(2000,12,21)
END_OF_WINTER   = datetime.date(2000,3,19)

START_OF_SPRING = datetime.date(2000,3,20)
END_OF_SPRING   = datetime.date(2000,6,20)

START_OF_SUMMER = datetime.date(2000,6,21)
END_OF_SUMMER   = datetime.date(2000,9,22)

START_OF_FALL = datetime.date(2000,9,23)
END_OF_FALL   = datetime.date(2000,12,20)