import time

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import ai
from eitaa_types import Message
from eitaa_types import Channel


class EitaaToolKit:
    """An utility class related to the internship task"""

    def __init__(self, channel_ids: list[str], phone_numbers: list[int] = []) -> None:
        self.phone_numbers = phone_numbers
        self.channel_ids = channel_ids

    def selenium_login_session(self):
        """Logs-in to the Eitaa's web app using the selenium's Firefox driver, for the goal
        of using the Global search feature."""

        raise NotImplementedError(
            """This method is currently incomplete. Eitaa's Global Search is
            barely accessable, even for it's own official clients."""
        )

        for phone_number in self.phone_numbers:
            print("Selenium is going to bootstrap. Please wait...")

            driver = webdriver.Firefox()
            driver.get("https://web.eitaa.com")
            wait = WebDriverWait(driver, 20)

            elem = wait.until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "input-field-phone")
                )
            )

            elem = elem.find_element(By.CLASS_NAME, "input-field-input")

            elem.click()

            elem.send_keys(str(phone_number))
            time.sleep(1)
            elem.send_keys(webdriver.Keys.ENTER)

            _ = wait.until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "rlottie")
                )  # Wait until the visibility of the eitaa's loading-like gif
            )

            otp_code = input(
                "Please provide the otp code that you've been recieved in your phone/current-eitaa-session : "
            )

    @staticmethod
    def get_latest_messages_by_id(channel_id: str) -> list[Message]:
        """Returns a list of messages."""

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://eitaa.com/{channel_id}", headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        pure_messages = soup.find_all(
            "div", attrs={"class": "etme_widget_message_bubble"}
        )

        messages: list[Message] = []

        for message in pure_messages:
            message_text = message.find(
                "div", attrs={"class": "etme_widget_message_text"}
            )

            views_element = message.find(
                "span", attrs={"class": "etme_widget_message_views"}
            )

            views = views_element.text.strip() if views_element else None

            image_link = message.find(
                "a", attrs={"class": "etme_widget_message_photo_wrap"}
            )

            image_url = None
            if image_link:
                style = str(image_link.get("style", ""))
                url_match = re.search(r"url\('([^']+)'\)", style)
                if url_match:
                    image_url = url_match.group(1)
                    if not image_url.startswith("http"):
                        image_url = f"https://eitaa.com{image_url}"

            pure_time = message.find("span", class_="etme_widget_message_meta")

            iso_time = None
            message_number = None

            if pure_time and pure_time.a:
                time_tag = pure_time.a.find("time")
                iso_time = time_tag.get("datetime") if time_tag else None
                href = pure_time.a.get("href", "")
                message_number = href.split("/")[-1] if href else None

            msg: Message = {
                "image_url": image_url if image_url else None,
                "text": message_text.get_text(separator="\n", strip=True)
                if message_text
                else None,
                "views": views,
                "iso_time": str(iso_time) if iso_time else "unknown",
                "message_number": int(message_number) if message_number else 0,
            }
            messages.append(msg)

        return messages

    def fetch_and_iterate(self) -> list[Channel]:
        """Fetches the latest messages from the channel_ids list"""

        channels: list[Channel] = []
        for id in self.channel_ids:
            messages = self.get_latest_messages_by_id(id)
            channel = Channel(id, messages)

            channels.append(channel)

        return channels

    def validate(self, channels: list[Channel]) -> list[Channel]:
        """Validates a list of channels with the help of openai, and then, returns the legit ones."""
        legit_ones: list[Channel] = []
        for channel in channels:
            legit = ai.classify_channel(channel)
            if legit:
                legit_ones.append(channel)

        return legit_ones
