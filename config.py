from datetime import timedelta

SECRET_KEY = "0ql7QxEB8P0ogjVfSX7Gvb95773Q0xkJGWf4lpq2yqVmIizzdo1z4yRailLsrb7W"
SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(days=5)
