import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from endpoints import NEW_EMAIL, MESSAGE_AFTER, MESSAGE_COUNT

class Mail(object):
    """
    Python wrapper for 10minutemail.com
    """

    def __init__(self):
        self.driver = None
        self.message_count = 0
        self.messages = []
        self.mail = None
        self.start_driver()

    def start_driver(self):
        options = Options()
        # options.add_argument("--headless")  # todo make headless
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1, 1)
        json_data = self.get_page(NEW_EMAIL)
        self.mail = json_data['address']

    def get_page(self, url):
        self.driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        json_data = json.loads(soup.find('pre').get_text())
        return json_data

    def get_mail(self):
        """
        :return: Mail of the current instance
        """
        return self.mail

    def get_message(self):
        """
        :return: list of messages stored in this instance
        """
        return self.messages

    def fetch_message(self):
        """
        Fetches for new messages which are not present in the instance
        :return: List of messages stored in the instance
        """
        res = self.get_page(MESSAGE_AFTER + str(self.message_count))
        self.message_count += len(res)
        self.messages += res
        return self.messages

    def new_message(self):
        """
        Check whether there are new messages or not
        :return: bool
        """
        return self.get_page(MESSAGE_COUNT)['messageCount'] != self.message_count

    def print_new_messages(self):
        if self.new_message():
            bodies = self.fetch_message()
            for body in bodies:
                sender = body['sender']
                subject = body['subject']
                text = body['bodyPlainText']
                print(f'from: {sender}')
                print(f'subject: {subject}')
                print(f'text: {text}')

    def __str__(self):
        return self.mail


if __name__ == "__main__":
    import time
    mail = Mail()
    print(mail.get_mail())
    while True:
        mail.print_new_messages()
        time.sleep(2)