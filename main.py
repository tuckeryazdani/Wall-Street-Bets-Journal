# Module Imports
from variables import *
import wsb

# Library Imports
import os
# import subprocess

def write_to_website(tweet:str):
    'Opens the Twitter HTML and adds the new tweet in it as a HTML blockquote with custom styling. (CSS file in website repo)'
    # Open file for reading and writing (r+)
    with open(TWITTER_PATH,'r+') as file:
        # Read HTML file in as a string.
        file_contents = file.read()
        # Set pointer to the beginning of the file.
        file.seek(0)
        # <body> Incidates where the new tweets should appear. 
        new_post_begin_index = file_contents.index('<body>')+len('<body>')
        # Add the tweet to the HTML Twitter page between <body> and </body> as a string.
        file_contents = file_contents[:new_post_begin_index] + '\n\n<br><br> <blockquote class="twitter-tweet">'+tweet.replace('\n','<br>')+'</blockquote>' + file_contents[new_post_begin_index:]
        # Overwrite the previous version of the HTML Twitter file with the newly added tweet.
        file.write(file_contents)
    
def push_to_git():
    'Pushes all changes to git'
    os.system('git add --all')
    os.system('git commit -m "Added new post"')
    os.system(f'git push origin {GIT_BRANCH}')

if __name__ == '__main__':
    
    tweet = wsb.main()

    # Change working directory to use the repository of the website.
    os.chdir(WEBSITE_REPO_PATH)

    # Ensure that the repo is updated.
    os.system(f'git pull origin {GIT_BRANCH}')

    # Add the twitter post to the twitter HTML page.
    write_to_website(tweet)
    
    # Push changes to git.
    push_to_git()