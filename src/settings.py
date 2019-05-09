import os

from dotenv import load_dotenv

load_dotenv()
RUNNING_TEST = os.getenv('RUNNING_TEST')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
