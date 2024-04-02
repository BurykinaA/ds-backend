from requests.exceptions import Timeout
import requests

class ImageProviderClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_image(self, image_id):
        url = f"{self.base_url}/images/{image_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except Timeout:
            return None
