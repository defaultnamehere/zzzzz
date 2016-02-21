
import datetime
import os

import history
import fbapi
import status


LOG_DATA_DIR = "log"
CSV_OUTPUT_DIR = "generated_graphs/csv"

# LOL TIMEZONES TOO HARD
UTC_OFFSET = 11

ONE_DAY_SECONDS = 60 * 60 * 24

class Grapher():

    def __init__(self):
        if not os.path.exists(CSV_OUTPUT_DIR):
            os.makedirs(CSV_OUTPUT_DIR)

    def to_csv(self, uid, start_time, end_time):

        # The user's history.
        status_history = history.StatusHistory(uid)

        # Their Facebook username.
        #uname = fbapi.get_user_name(uid)


        # Generate a CSV from the multiple linear timeseries
        with open("generated_graphs/csv/{uid}.csv".format(uid=uid), "w") as f:

            f.write("time,")
            f.write(",".join(status.Status.statuses))
            f.write("\n")

            # TODO preprocess sort and splice this instead of linear search.
            # UPDATE nahhhh I think I'll just commit it to github ;>_>
            for data_point in status_history.activity:
                if start_time < data_point.time < end_time:
                    # Write the time.
                    f.write(str(data_point.time) + ",")
                    # Write the various statuses.
                    # Sample line: <time>,3,1,1,1,1
                    f.write(",".join(str(data_point._status[status_type]) for status_type in status.Status.statuses))
                    f.write("\n")


    def generate_all_csvs(self, start_time, end_time):
        for filename in os.listdir(LOG_DATA_DIR):
            print(filename)
            uid = filename.split(".")[0]
            self.to_csv(uid, start_time, end_time)


if __name__ == "__main__":
    g = Grapher()

    now = history.StatusHistory.START_TIME
    # Graph the last three days by default, but you can do ~whatever you believe you cannnnn~
    g.generate_all_csvs(start_time=now - 3 * ONE_DAY_SECONDS, end_time=now)
