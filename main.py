from data import Data
from picture import Picture
from post import Post


import logging
from const import LOGGING_FORMAT

logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)




def main():
    data = Data().get_post()
    Picture(data[0], data[1], data[2]).get_picture()
    Post().create_post()


if __name__ == "__main__":
    main()
