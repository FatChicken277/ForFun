#!/usr/bin/python3
"""This module contains a methods that generates a
    random fortune cookie message with help of web scrapping.
"""
import requests
from bs4 import BeautifulSoup

DOMAIN = "http://www.fortunecookiemessage.com/"


def web_connection(sub_page=""):
    """CONNECT TO WEBSITE"""

    response = requests.get(DOMAIN + sub_page)
    if response.status_code != 200:
        raise SystemExit("Could not connect satisfactorily to the website")
    return response


def fortune_cookie():
    """GENERATE A RANDOM FORTUNE COOKIE MESSAGE."""

    fortune_html = web_connection().text
    fortune_soup = BeautifulSoup(fortune_html, "html.parser")

    fortune_body = fortune_soup.find("div", id="bodycontent")
    fortune_message = fortune_body.find("div", id="message")
    fortune_message = fortune_message.find("div", class_="quote").a

    print(fortune_message.text)


if __name__ == "__main__":
    fortune_cookie()
