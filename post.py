import vk_api
import logging
from const import *


class Post:
    def __init__(self):
        self.vkSession = vk_api.VkApi(token=ACCESS_TOKEN)
        logging.info("Successfully created vk session")

        photo_list = vk_api.VkUpload(self.vkSession).photo_wall(OUTPUT_PATH)
        self.photo = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
        logging.info("Photo id was received")

    def create_post(self):
        self.vkSession.method("wall.post", {
            'owner_id': '-' + str(GROUP_ID),
            'message': POST_MESSAGE,
            'attachment': self.photo
        })
        logging.info("Post has been created")
