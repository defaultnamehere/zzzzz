
import requests

import fetcher


def get_user_name(fbid):
    resp = requests.get("https://www.facebook.com/app_scoped_user_id/" + str(fbid), headers=fetcher.Fetcher.REQUEST_HEADERS, allow_redirects=True)
    return resp.url.split("/")[-1]

