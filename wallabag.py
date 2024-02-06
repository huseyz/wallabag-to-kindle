import re
import requests


class Wallabag:
    def __init__(self, server, client_id, client_secret, username, password):
        self.server = server
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    def get_token(self):
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(f"{self.server}/oauth/v2/token", data)
        return response.json()["access_token"]

    def get_entries(self, token, tags=[], perPage=30, page=1):
        headers = {"Authorization": f"Bearer {token}"}
        params = {"perPage": perPage, "page": page, "tags": ",".join(tags)}
        response = requests.get(
            f"{self.server}/api/entries.json", params=params, headers=headers
        ).json()
        items = response["_embedded"]["items"]
        ids = [item["id"] for item in items]
        if response["page"] == response["pages"]:
            return ids
        else:
            return ids + self.get_entries(token, tags, perPage, page + 1)

    def get_epub(self, token, id):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{self.server}/api/entries/{id}/export.epub", headers=headers
        )
        filename = re.findall(
            'filename=["](.+)["]', response.headers.get("content-disposition")
        )[0]
        return {"name": filename, "content": response.content}
