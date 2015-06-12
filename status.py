from collections import defaultdict
import cPickle as pickle
# This Class Implement the status object,it encapsulate the map cache


class SeasonFactory:
    def __call__(self, *args, **kwargs):
        return defaultdict(list)


class Status:
    __status_file_name = "status.plk"
    __empty_status = ""
    __status = defaultdict(SeasonFactory())  # dichiarato defaultdict

    def __init__(self):
        try:
            with open(self.__status_file_name, 'rb') as infile:
                self.__status = pickle.load(infile)
        except IOError:
            self.__empty_status = True

    def get_status(self):
        if self.__empty_status:
            return None
        else:
            self.reload_status()
            return self.__status

    def add_episode(self, series, season, episode):
        self.__status[series][season].append(episode)

    def write_status(self):
        with open(self.__status_file_name, 'wb') as outfile:
            pickle.dump(self.__status, outfile)
        if self.__empty_status:
            self.__empty_status = False
        self.reload_status()

    def reload_status(self):
        with open(self.__status_file_name, 'rb') as infile:
            self.__status = pickle.load(infile)


if __name__ == "__main__":
    st = Status()
    print st.get_status()
