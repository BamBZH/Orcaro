from utils import prtWarning, prtInfo

MISSION_SPENT_TIME_STR = "mission_spent_time"
TOTAL_STR = "total"
UNKNOWN_CATEGORY_STR = "UNKNOWN_CATEGORY"
DATES_STR = "dates"


class DataModel:
    """
    This class represents the Data Model of the Outlook events
    """

    def __init__(self, events):
        self.events = events
        self.time_per_mission = {}
        self.ratio_per_mission = {}

    def show_events(self):
        prtInfo("\n*** Events fetched ***")
        for idx, event in enumerate(self.events):
            print(f"Event[{idx}] : {event}")
            if len(event.categories) == 0:
                category = UNKNOWN_CATEGORY_STR
            else:
                category = event.categories[0]
            print(f"\tCategory : {category}")
            print(f"\tSpent time : {self.diff_time_spent(event)}")

    def show_time_per_mission(self):
        prtInfo("\n*** Time per mission table ***")
        for day, value in self.time_per_mission.items():
            print(f"* Day {day} - Total in hours ({value[TOTAL_STR]}) :")
            for mission, time_spent in value[MISSION_SPENT_TIME_STR].items():
                print(f"\t* Mission '{mission}' - Time spent in hours : {time_spent}")

    def show_ratio_per_mission(self):
        prtInfo("\n*** Ratio per mission table ***")
        for mission, value in self.ratio_per_mission.items():
            print(f"* Mission {mission} - Total in hours ({value[TOTAL_STR]}) :")
            for date, ratio in value[DATES_STR].items():
                print(f"\t* Date '{date}' - Time spent in hours : {ratio}")

    def sort_events(self) -> list:

        if not self.events:
            prtWarning("Events list empty.")
        else:
            sorted_events = []
            for event in self.events:
                sorted_events.append(event)
            sorted_events.sort(key=lambda x: x.start)

            self.events = sorted_events

        return self.events

    def compute_time_spent(self) -> dict:
        """ Compute the mission ratios per day

        :return:
        Ex :
        { "1" : { "mission_spent_time" : {"MissionX" : 2, "MissionY" : 2}, "Total" : 4 } },
        "2" : : { "MissionX" : 4}, "Total" : 4 } }
        }
        """
        tpm = self.time_per_mission
        for event in self.events:
            day = event.start.strftime("%d/%m/%y")
            day = str(day)
            if len(event.categories) == 0:
                category = UNKNOWN_CATEGORY_STR
            else:
                category = event.categories[0]
            time_spent = self.diff_time_spent(event)
            if day in tpm:
                if category in tpm[day][MISSION_SPENT_TIME_STR]:
                    self.time_per_mission[day][MISSION_SPENT_TIME_STR][category] += time_spent
                    self.time_per_mission[day][TOTAL_STR] += time_spent
                else:
                    self.time_per_mission[day][MISSION_SPENT_TIME_STR][category] = time_spent
                    self.time_per_mission[day][TOTAL_STR] += time_spent
            else:
                tpm[day] = {MISSION_SPENT_TIME_STR: {category: time_spent}, TOTAL_STR: time_spent}

        return tpm

    def compute_ratios(self) -> dict:

        tpm = self.time_per_mission
        rpm = self.ratio_per_mission
        for day in tpm.keys():
            for mission_key, mission_value in tpm[day][MISSION_SPENT_TIME_STR].items():
                ratio = mission_value / tpm[day][TOTAL_STR]
                if mission_key in rpm.keys():
                    rpm[mission_key][DATES_STR][day] = ratio
                    rpm[mission_key][TOTAL_STR] += ratio
                else:
                    rpm[mission_key] = {DATES_STR: {day: ratio}, TOTAL_STR: ratio}

        return rpm

    @staticmethod
    def diff_time_spent(event) -> int:
        time_spent = event.end - event.start
        return time_spent.seconds / 3600
