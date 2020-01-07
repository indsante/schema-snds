import os

from dotenv import load_dotenv

load_dotenv()
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
