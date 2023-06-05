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

Docker container instructions:<br>
Run the following commands<br>
<br>
Build a docker container. You can change the name "wsb_journal" to whatever name you might like.<br>
docker build -t wsb_journal .
<br>
Then we run the container.<br>
docker run --name wsb_journal wsb_journal<br>
<br>
Note that due to this being a public repository I have removed the variables.py file which contains various API keys for this project.