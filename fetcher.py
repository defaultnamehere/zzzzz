import argparse as ap
import json
import os
import time

import requests

import graph


secrets = ap.Namespace()

# Load the secrets from file so some scrublord like me doesn't accidentally commit them to git.
with open("SECRETS.txt") as f:
    for line in f:
        vals = line.strip().split('=', 1)
        setattr(secrets, vals[0].lower(), vals[1])


SLEEP_TIME = 1

OFFLINE_STATUS_JSON = """{"lat": "offline", "webStatus": "invisible", "fbAppStatus": "invisible", "otherStatus": "invisible", "status": "invisible", "messengerStatus": "invisible"}"""
ACTIVE_STATUS_JSON = """{ "lat": "online", "webStatus": "invisible", "fbAppStatus": "invisible", "otherStatus": "invisible", "status": "active", "messengerStatus": "invisible"}"""

class Fetcher():
    # Headers to send with every request.
    REQUEST_HEADERS = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'en-US,en;q=0.8,en-AU;q=0.6',
        'cookie': secrets.cookie,
        'dnt': '1',
        'origin': 'https://www.facebook.com',
        'referer': 'https://www.facebook.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
    }

    # Hey hey, Facebook puts this in front of all their JSON to prevent hijacking. But don't worry, we're ~verified secure~.
    JSON_PAYLOAD_PREFIX = "for (;;); "

    def __init__(self):
        if not os.path.exists(graph.LOG_DATA_DIR):
            os.makedirs(graph.LOG_DATA_DIR)
        self.reset_params()
        self.excludes = []
        if hasattr(secrets, 'excludes'):
            self.excludes = secrets.excludes.split(',',1)

    def make_request(self):
        # Load balancing is for chumps. Facebook can take it.
        url = "https://5-edge-chat.facebook.com/pull"
        response_obj = requests.get(url, params=self.params, headers=self.REQUEST_HEADERS)

        try:
            raw_response = response_obj.text
            if not raw_response:
                return None
            if raw_response.startswith(self.JSON_PAYLOAD_PREFIX):
                data = raw_response[len(self.JSON_PAYLOAD_PREFIX) - 1:].strip()
                data = json.loads(data)
            else:
                # If it didn't start with for (;;); then something weird is happening.
                # Maybe it's unprotected JSON?
                data = json.loads(raw_response)
        except ValueError as e:
            print(str(e))
            return None

        print("Response:" + str(data))

        return data


    def _log_lat(self, uid, lat_time):
        if not uid in self.excludes:
            with open("log/{uid}.txt".format(uid=uid), "a") as f:
                # Now add an online status at the user's LAT.
                user_data = []
                user_data.append(lat_time)
                user_data.append(ACTIVE_STATUS_JSON)
                f.write("|".join(user_data))
                f.write("\n")

                # Assume the user is currently offline, since we got a lat for them. (This is guaranteed I think.)
                user_data = []
                user_data.append(str(time.time()))
                user_data.append(OFFLINE_STATUS_JSON)
                f.write("|".join(user_data))
                f.write("\n")



    def start_request(self):
        print(">")
        resp = self.make_request()
        if resp is None:
            print("Got error from request, restarting...")
            self.reset_params()
            return

        # We got info about which pool/sticky we should be using I think??? Something to do with load balancers?
        if "lb_info" in resp:
            self.params["sticky_pool"] = resp["lb_info"]["pool"]
            self.params["sticky_token"] = resp["lb_info"]["sticky"]

        if "seq" in resp:
            self.params["seq"] = resp["seq"]

        if "ms" in resp:
            for item in resp["ms"]:
                # The online/offline info we're looking for.

                if item["type"] == "buddylist_overlay":

                    # Find the key with all the message details, that one is the UID.
                    for key in item["overlay"]:
                        if type(item["overlay"][key]) == dict:
                            uid = key

                            # Log the LAT in this message.
                            self._log_lat(uid, str(item["overlay"][uid]["la"]))

                            # Now log their current status.
                            if "p" in item["overlay"][uid]:
                                with open("log/{uid}.txt".format(uid=uid), "a") as f:
                                    user_data = []
                                    user_data.append(str(time.time()))
                                    user_data.append(json.dumps(item["overlay"][uid]["p"]))
                                    f.write("|".join(user_data))
                                    f.write("\n")

                # This list contains the last active times (lats) of users.
                if "buddyList" in item:
                    for uid in item["buddyList"]:
                        if "lat" in item["buddyList"][uid]:
                            self._log_lat(uid, str(item["buddyList"][uid]["lat"]))



    def reset_params(self):
        self.params = {
            # No idea what this is.
            'cap': '8',
            # No idea what this is.
            'cb': '2qfi',
            # No idea what this is.
            'channel': 'p_' + secrets.uid,
            'clientid': secrets.client_id,
            'format': 'json',
            # Is this my online status?
            'idle': '0',
            # No idea what this is.
            'isq': '173180',
            # Whether to stream the HTTP GET request. We don't want to!
            # 'mode': 'stream',
            # Is this how many messages we have got from Facebook in this session so far?
            # Previous value: 26
            'msgs_recv': '0',
            # No idea what this is.
            'partition': '-2',
            # No idea what this is.
            'qp': 'y',
            # Set starting sequence number to 0.
            # This number doesn't seem to be necessary for getting the /pull content, since setting it to 0 every time still gets everything as far as I can tell. Maybe it's used for #webscale reasons.
            'seq': '0',
            'state': 'active',
            'sticky_pool': 'atn2c06_chat-proxy',
            'sticky_token': '0',
            'uid': secrets.uid,
            'viewer_uid': secrets.uid,
            'wtc': '171%2C170%2C0.000%2C171%2C171'
        }


if __name__ == "__main__":
    f = Fetcher()
    while True:
        try:
            f.start_request()
            time.sleep(SLEEP_TIME)
        except UnicodeDecodeError:
            f.reset_params()
            print("UnicodeDecodeError!")
