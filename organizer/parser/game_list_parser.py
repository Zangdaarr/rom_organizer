import os

from lxml import etree

from organizer.tools.exception_tools import ExceptionPrinter


class GameListParser(object):

    GAMELIST_FILE = 'gamelist.xml'

    __GAME_NODE       = "game"

    __ROOT_KEY        = "root"

    __EXCLUDE_FOLDERS = ['media']

    def __init__(self, gamelist_path):
        self.root       = gamelist_path
        self.gamelist   = os.path.join(gamelist_path, self.GAMELIST_FILE)

        self.games_nodes    = []
        self.files_to_parse = []

        self.parsed_gamelist = None

    def parse(self):
        parser = etree.XMLParser(remove_blank_text=True)

        try:
            self.parsed_gamelist = etree.parse(self.gamelist, parser)
        except Exception as something_happened:
            ExceptionPrinter.print_exception(something_happened)

        self.__process_games_nodes()
        self.validate()

    def write_document(self):
        self.validate()
        self.parsed_gamelist.write(self.gamelist, pretty_print=True)

    def validate(self):
        for game in self.get_all_games_nodes():
            game_path = os.path.join(self.root, game.get_path(game))

            if not os.path.isfile(game_path):
                raise Exception("No game file located at %s", game_path)

    def get_root(self):
        return self.root

    def get_all_files(self):
        if not self.files_to_parse:
            self.__process_all_files_to_parse()

        return self.files_to_parse

    def get_all_games_nodes(self):
        if not self.games_nodes:
            self.__process_games_nodes()

        return self.games_nodes

    def get_game_node_from_game_file(self, name):

        game_node = None

        for game in self.get_all_games_nodes():
            path = game.get_path(game)
            _, file_name = os.path.split(path)

            if file_name == name:
                game_node = game

        return game_node

    def __process_games_nodes(self):
        if self.parsed_gamelist is None:
            self.parse()

        for node in self.parsed_gamelist.findall(self.__GAME_NODE):
            self.games_nodes.append(node)

    def __process_all_files_to_parse(self):

        self.files_to_parse = []

        for root, dirs, names in os.walk(self.root):

            path_contains_excluded_folder = any(value in root for value in self.__EXCLUDE_FOLDERS)

            if not path_contains_excluded_folder:

                for name in names:
                    self.files_to_parse.append(name)


