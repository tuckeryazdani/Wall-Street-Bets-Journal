# WSB_Journal ( Wall Street Bets Journal )

This project is fully automated in Python using various APIs to pull data, get stock market updates depending on that data, getting seasonal information on how that stock performs in the given and next season, and then posting that data to Twitter. I have updated this program to be able to then take that tweet, add it to the Twitter website HTML page in Python, and then push the changes using git in the os Python library, so that it will now show up here as well for logging purposes.<br>
<br>
The Twitter account will also respond with funny responses if you tweet at it that are AI generated from ChatGPT 3.5. Warning: These responses are completely AI generated.<br>
<br>
Technologies Used:
<br>
Languages : <i> Python, HTML, CSS </i>
<br>
Libraries : <i> pandas, datetime, requests, io, typing, warnings, yfinance, praw, tweepy, openai </i>
<br>

Docker container instructions:
Run the following commands

Build a docker container. You can change the name "wsb_journal" to whatever name you might like.
docker build -t wsb_journal .

Then we run the container.
docker run --name wsb_journal wsb_journal