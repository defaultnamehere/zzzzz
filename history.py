
import bisect
import time

import status


class StatusHistory():
    """Object representing the history for a particular user. History stored sparse."""


    EPOCH_TIME = 1452556800

    # Save the start time so computation time doesn't offset the measured time.
    START_TIME = int(time.time())

    def __init__(self, uid):
        with open("log/{uid}.txt".format(uid=uid)) as f:
            self.activity = self.parse_status(map(str.strip, f.readlines()))

    def create_time_map(self, status_list):
        status_map = {}
        for item in status_list:
            status_map[int(float(item["time"]))] = item["status"]
        return status_map

    def parse_status(self, lines):
        # A list of status objects.
        activity = []

        # Keep a list of seen times so we can avoid duplicates in the history
        seen_times = set()

        for line in lines:
            time, fields = line.split("|")
            # Only add new times, preferring earlier records in the file. This is probably not optimal since later records seem to be more likely to be LATs, but oh well gotta break a few algorithmic contraints to make a BILLION dollars.
            if time not in seen_times:
                seen_times.add(time)
                status_obj = status.Status(int(float(time)), fields)
                activity.append(status_obj)
        return activity

    def get_status(self, time):
        """Get the HAST (highest active status type) for the user at a particular time by querying the sparse data."""
        # #ALGORITHMS
        # This index is the index of the item AFTER this item would go if it were inserted.
        idx = bisect.bisect(self.activity, time)

        # Since we treat status data points as valid until the next data point, the "current" status is the one on the left of where the inserted time would go.
        current_status = self.activity[max(0, idx - 1)]

        return current_status


    def normalised(self, max_time_back_seconds=None, resolution=60, status_type=None):
        """Turns a sparse time series into a dense one, with number of seconds per bucket specified by resolution.
        If a status_type (status, webStatus, messengerStatus etc.) is given, returns a generator of the status level (online, offline, idle) for that status type."""

        if max_time_back_seconds is None:
            start_time = self.EPOCH_TIME
        else:
            start_time = self.START_TIME - max_time_back_seconds

        for tick in range(start_time, self.START_TIME, resolution):
            status_obj = self.get_status(tick)
            if status_type is None:
                yield status_obj.highest_active_status_type()
            else:
                yield status_obj._status[status_type]



