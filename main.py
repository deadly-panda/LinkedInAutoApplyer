from selenium import webdriver
import json

from src import app


if __name__ == "__main__":
    with open('config.json') as f:
        data = json.load(f)

    easy_applyer = app.EasyApplyer(data)
    easy_applyer.run()
