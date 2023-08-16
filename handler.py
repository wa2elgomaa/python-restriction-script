""" handler.py """
import time
from datetime import datetime
from traceback import print_exc
from pydash import get, set_with
from logger import Logger
from dotenv import dotenv_values
from requester import Requester


class Handler:
    environment = 'sandbox.thenational'
    sources = ['AFP', 'Bloomberg', 'Reuters', 'Associated Press']
    source_type = 'wires'

    def __init__(self, environment, debug=False):
        self.photos_list = []
        self.environment = environment
        env_file = '.env' if environment == 'prod' else '.env.sandbox'
        self.env_config = dotenv_values(env_file)
        self.logger = Logger(debug_mode=debug)

        self.requester = Requester(self.env_config)

    def search(self, start_date, end_date, offset=0, limit=100):
        url = f'{self.env_config.get("API_BASE")}/photo/api/v2/photos/?offset={offset}&limit={limit}&published=true' \
              f'{self.env_config.get("SOURCES")}&sort=created_date&quality=1&total=1&restricted=false' \
              f'&startDateUploaded={start_date}&endDateUploaded={end_date}'
        self.logger.log_message(f'Requesting query : {url}')

        try:
            response = self.requester.fetch(url=url)
            if get(response, 'error', None) is None:
                self.photos_list = response
                self.logger.log_message(f'Loaded the photos list with length {len(self.photos_list)}')
            else:
                self.logger.log_message(f'Failed to load photos list {get(response, "error")}')

        except any as e:
            print(e)
            msg = f'ERR loading photos list {url} with error {print_exc()}'
            self.logger.log_message(msg, e)

        return self

    def save_photo(self, photo):
        try:
            url = f'{self.env_config.get("API_BASE")}/photo/api/v2/photos/{get(photo, "_id")}'
            response = self.requester.put(url, photo)
            return response
        except any as e:
            print(e)
            self.logger.log_message(f'Saving photo error {print_exc()}', e)
            raise e

    def restrict(self, photo=None):
        if (photo is not None  # if the photo exists
                and get(photo, 'source.source_type', '') == self.source_type  # if the photo is a wired source
                and get(photo, 'additional_properties.restricted',
                        False) is False  # if the photo not restricted already
                and get(photo, 'source.name', 'Any') in self.sources  # if it is one of the 4 wired types
                and get(photo, 'additional_properties.restriction_date', None) is None  # if restriction date is empty
                and get(photo, 'additional_properties.published', False) is True  # if photo is published
        ):
            # should restrict this photo
            restriction_date = datetime.now().isoformat()
            version = get(photo, 'additional_properties.version', 0)
            set_with(photo, 'additional_properties.restriction_date', restriction_date)
            set_with(photo, 'additional_properties.restricted', True)
            set_with(photo, 'additional_properties.version', ++version)

            try:
                # put the new photo data
                response = self.save_photo(photo)

                if get(response, 'error', None) is None:
                    # successful 
                    self.logger.log_message(f'Photo {get(photo , "_id")} has been updated')
                else:
                    # log error
                    self.logger.log_message(f'Photo {get(photo , "_id")} '
                                            f'failed to update with error {get(response, "error")}')
                return True
            except any as e:
                print(e)
                msg = f'ERR restricting photo {get(photo , "_id")} with error {print_exc()}'
                self.logger.log_message(msg, e)

        return False

    def update(self):
        try:
            self.logger.log_message(f'Updating photo list with length {len(self.photos_list)}')
            if len(self.photos_list) > 0:
                for photo in self.photos_list:
                    if photo['_id'] is not None:
                        self.logger.log_message(f'Processing Image {photo["_id"]}')
                        time.sleep(2)
                        # restrict this photo
                        self.restrict(photo)
                return False
            else:
                return True
        except any as e:
            print(e)
            msg = f'ERR while processing photos with error {print_exc()}'
            self.logger.log_message(msg, e)
        return False
