import os
API_AUTH_TOKEN = os.getenv('GITHUB_AUTH_TOKEN')
DB_NAME = os.getenv('DB_NAME', '../instance/test.db')
