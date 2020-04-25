import datetime
from bs4 import BeautifulSoup
import requests
import logging

from const import *


class Data:
    def __init__(self):
        self.celebrations = []
        self.historical_events = []

        if 'zavtra' not in CITE:
            self.date = (datetime.datetime.now()).strftime(DATE_FORMAT)
        else:
            # Got a tomorrow date
            self.date = (datetime.date.today() + datetime.timedelta(days=1))
            self.date = self.date.strftime(DATE_FORMAT)

    def __delete_bullets(self, list_to_change):
        result = []

        for i in range(len(list_to_change)):
            result.append(list_to_change[i].replace(DOT, ''))

        logging.info("Dots have been deleted")
        return result

    def __get_celebrations(self):
        html = requests.get(CITE, headers=HEADERS).content
        logging.info("Successfully get a content for celebrations"); logging.info(html)
        bs = BeautifulSoup(html, "lxml")
        celebrations = bs.find('div', {'class': 'listing_wr'})

        result = []
        for child in celebrations.contents:
            try:
                try:
                    celebration_date = child.div.find('span', {'class': 'super'}).text
                    child.div.find('span', {'class': 'super'}).decompose()
                    result.append(child.text.decode('utf8') + ' ({})'.format(celebration_date))
                # It's magic, but it won't work without it
                finally:
                    result.append(child.text)
            except AttributeError:
                pass

        self.celebrations = self.__delete_bullets(result[:])
        logging.info("All celebrations have been added")

    def __get_historical_events(self):
        html = requests.get(CITE, headers=HEADERS).content
        logging.info("Successfully get a content for historical events")
        bs = BeautifulSoup(html, "lxml")
        history = bs.find('div', {'class': 'event_block'})

        result = []
        for child in history.contents:
            try:
                # Site features
                if 'zavtra' not in CITE:
                    event_date = child.span.text
                    event = child.text.replace(event_date, '')
                    result.append('{} ({})'.format(event, event_date))
                else:
                    event = child.text
                    result.append(event)
            except AttributeError:
                pass

        self.historical_events = self.__delete_bullets(result[:])
        logging.info("All historical events have been added")

    def get_post(self):
        self.__get_celebrations()
        self.__get_historical_events()
        logging.info("All data have been prepared")
        return [self.celebrations,
                self.historical_events,
                self.date]
