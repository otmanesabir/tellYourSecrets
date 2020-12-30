from models import app_info
from config import global_config
import abc
import logger
import enum

log = logger.setup_custom_logger(__name__)
scraper_cfg = global_config.global_config.get_instance().CFG["crawler_settings"]

class crawler_types(enum.Enum):
   PLAY_STORE = 1
   APP_STORE = 2
   ALL = 3

class crawler_interface(metaclass=abc.ABCMeta):
    MAX_REVIEWS = scraper_cfg["review_limit"]
    APP_LIMIT = scraper_cfg["app_limit"]

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_reviews') and 
                callable(subclass.get_reviews) and 
                hasattr(subclass, 'search_app_name') and 
                callable(subclass.search_app_name) or 
                NotImplemented)

    @abc.abstractmethod
    def get_reviews(self, app_info: app_info.app_info):
        """Get reviews of a given app from the implementing class"""
        raise NotImplementedError

    @abc.abstractmethod
    def search_app_name(self, app_name: str, start_idx: int):
        """Searches an app name in the implementing class"""
        raise NotImplementedError

    