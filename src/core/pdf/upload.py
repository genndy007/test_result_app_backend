

from filestack import Client

from src.config import Config


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonFilestack(metaclass=SingletonMeta):
    def __init__(self):
        self.client = Client(Config.FILESTACK_API_KEY)

    def upload_pdf(self, full_path):
        store_params = {
            "mimetype": "application/pdf"
        }
        new_filelink = self.client.upload(filepath=full_path, store_params=store_params)
        return new_filelink.url



