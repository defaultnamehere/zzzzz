import json

class StatusLevel():
    OFFLINE = 0
    INVISIBLE = 1
    IDLE = 2
    ACTIVE = 3


class Status():
    """The status of a user."""

    value_map = {
        "offline": StatusLevel.OFFLINE,
        "invisible": StatusLevel.INVISIBLE,
        "idle": StatusLevel.IDLE,
        "active": StatusLevel.ACTIVE
    }

    statuses = "status webStatus messengerStatus fbAppStatus otherStatus".split()

    status_type_map = {
        "status": 4,
        "webStatus": 3,
        "messengerStatus": 2,
        "fbAppStatus": 1,
        "otherStatus": 0
    }


    def __init__(self, time, status_json):

        self.time = time
        self._status = {}
        self.lat = False

        fields = json.loads(status_json)

        for status in self.statuses:
            # Map status_name -> status value enum
            self._status[status] = self.value_map[fields[status]]

        # Is this an entry for a last active time?
        if "lat" in fields:
            self.lat = True

    def is_online(self):
        return self._status["status"] == StatusLevel.ACTIVE

    def all_active_status_types(self):
        """Returns all status types which are currently active. If types other than "status" are active, "status" is necessarily also active."""

        return filter(lambda status_type: self._status[status_type] >= StatusLevel.ACTIVE, self._status.keys())

    def highest_active_status_type(self):
        active_status_types = list(self.all_active_status_types())

        if not active_status_types:
            return 0

        return max([self.status_type_map[status] for status in active_status_types])

    # Make these objects sortable by time.
    def __lt__(self, other):
        return self.time < other

    def __gt__(self, other):
        return self.time > other
