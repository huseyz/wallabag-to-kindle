import os
from mailclient import MailClient
from wallabag import Wallabag


def main():
    wallabag = Wallabag(
        os.getenv("WALLABAG_SERVER"),
        os.getenv("WALLABAG_CLIENT_ID"),
        os.getenv("WALLABAG_CLIENT_SECRET"),
        os.getenv("WALLABAG_USERNAME"),
        os.getenv("WALLABAG_PASSWORD"),
    )
    email = MailClient(
        os.getenv("EMAIL_SERVER"),
        os.getenv("EMAIL_PORT"),
        os.getenv("EMAIL_USERNAME"),
        os.getenv("EMAIL_PASSWORD"),
        os.getenv("EMAIL_SEND_FROM", os.getenv("EMAIL_USERNAME")),
        os.getenv("EMAIL_SUBJECT", "Wallabag to Kindle"),
    )
    tags = os.getenv("WALLABAG_TAGS", "").split(",")

    print("Requesting Wallabag token.")
    token = wallabag.get_token()

    print("Requesting entries from Wallabag.")
    ids = wallabag.get_entries(token, tags)
    print(f"Received {len(ids)} articles.")

    already_synced = __get_already_synced()
    not_synced = set(ids) - set(already_synced)

    if not not_synced:
        print("No articles to sync.")
        return

    articles = [wallabag.get_epub(token, id) for id in not_synced]

    to = os.getenv("SEND_TO_KINDLE_EMAIL")
    print(f"Sending {len(articles)} articles to {to}.")
    email.send_files(to, articles)

    print(f"Synced.")
    __set_already_synced(set(ids + already_synced))


def __get_already_synced():
    path = os.getenv("SYNCED_FILE", "/data/synced")
    if not os.path.exists(path):
        open(path, "a").close()
    return [int(id) for id in open(path, "r").read().split(",") if id]


def __set_already_synced(ids):
    path = os.getenv("SYNCED_FILE", "/data/synced")
    open(path, "w").write(",".join([str(id) for id in ids]))


if __name__ == "__main__":
    main()
