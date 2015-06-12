import os
import re
import string
from status import Status
# This class can adapt the file name downloaded from the web into the Plex standard format


class FileAdapter:
    __dir_path = ""
    __plex_path = "/home/matteo/TV Shows/"
    __title_pattern = "(.)*.(s|S)([0-9]+)(e|E)([0-9]+)"
    __file_type_pattern = "(.avi\Z)|(.mkv\Z)|(.mp4\Z)|(.mpg\Z)"
    __series_pattern = "(([a-zA-Z]|\s)+)\s"
    __season_pattern = "((s|S)([0-9]+))"
    __episode_pattern = "((e|E)([0-9]+))"
    __files = []
    __status = None

    def __init__(self, dir_path):
        self.__dir_path = dir_path
        self.__status = Status()

    def set_path(self, dir_path):
        self.__dir_path = dir_path

    def get_path(self):
        return self.__dir_path

    def discover_list_file(self):
        for (dir_path, dir_names, file_names) in os.walk(self.__dir_path):
            for f in file_names:
                or_name, file_name, series, season, episode = self.match_file_name(f)
                if file_name:
                    self.__files.append((dir_path, or_name, file_name, series, season, episode))
        print self.__files

    def match_file_name(self, name):
        file_name = re.search(self.__title_pattern, name)
        file_type = re.search(self.__file_type_pattern, name)
        season = re.search(self.__season_pattern, name)
        episode = re.search(self.__episode_pattern, name)
        if file_name and file_type:
            return name, \
                   string.replace(file_name.group(0), '.', ' ') + file_type.group(0), \
                   (re.search(self.__series_pattern, string.replace(file_name.group(0), '.', ' ')).group(0).rstrip()), \
                   season.group(0), \
                   episode.group(0)
        else:
            return None, None, None, None, None

    def move_file(self):
        current_status = self.__status.get_status()
        if current_status:
            # there is a status file!I need to check if the file are already moved in the plex directory
            for item in self.__files:
                if item[3] in current_status and item[4] in current_status[item[3]] and item[5] in \
                        current_status[item[3]][item[4]]:
                    continue
                else:
                    self.__status.add_episode(item[3], item[4], item[5])
                    if not os.path.exists(self.__plex_path + item[3]):
                        os.makedirs(self.__plex_path + item[3])
                    if not os.path.exists(self.__plex_path + item[3] + "/Season " + item[4][-2:]):
                        os.makedirs(self.__plex_path + item[3] + "/Season " + item[4][-2:])
                    os.rename(item[0] +"/"+ item[1], self.__plex_path + item[3] + "/Season " + item[4][-2:] + "/" + item[2])
        else:
            # EmptyStatus
            for item in self.__files:
                self.__status.add_episode(item[3], item[4], item[5])
                if not os.path.exists(self.__plex_path + item[3]):
                    os.makedirs(self.__plex_path + item[3])
                if not os.path.exists(self.__plex_path + item[3] + "/Season " + item[4][-2:]):
                    os.makedirs(self.__plex_path + item[3] + "/Season " + item[4][-2:])
                os.rename(item[0] + "/" + item[1],
                          self.__plex_path + item[3] + "/Season " + item[4][-2:] + "/" + item[2])

        self.__status.write_status()


if __name__ == "__main__":
    file_adapter = FileAdapter("/home/matteo/")
    file_adapter.discover_list_file()
    file_adapter.move_file()
