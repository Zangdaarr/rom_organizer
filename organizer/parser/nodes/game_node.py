import re


class GameNode(object):

    __GENRE_ATTRIB    = "genre"
    __PATH_ATTRIB     = "path"
    __NAME_ATTRIB     = "name"

    __NO_GENRE  = "Unclassified"
    __NO_TEXT   = "Undefined_text"

    def __init__(self, node):
        self.__node = node

    def get_node(self):
        return self.__node

    def get_genre(self):
        match_any_slashes_or_space = re.compile(r'(?:\s+|\\+|/+)')
        match_any_caret = re.compile(r'-+')

        genre = self.__get_game_child_value(self.__GENRE_ATTRIB)

        genre = re.sub(match_any_slashes_or_space, '-', genre)
        genre = re.sub(match_any_caret, '-', genre)

        return genre if genre is not self.__NO_TEXT else self.__NO_GENRE

    def set_path(self, value):
        self.__set_game_child_value(self.__PATH_ATTRIB, value)

    def get_path(self):
        return self.__get_game_child_value(self.__PATH_ATTRIB)

    def get_name(self):
        return self.__get_game_child_value(self.__NAME_ATTRIB)

    def __get_attrib(self, key):
        return self.get_node().find(key)

    def __set_game_child_value(self, key, value):
        game_child = self.__get_attrib(key)

        if game_child is not None:
            game_child.text = value

    def __get_game_child_value(self, key):
        game_child = self.__get_attrib(key)

        if game_child is None or game_child.text is None:
            return self.__NO_TEXT
        else:
            return game_child.text