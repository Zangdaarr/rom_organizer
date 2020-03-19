from organizer.parser.game_list_parser import GameListParser
from organizer.parser.genre_aliases_generator import GenreAliasesGenerator


class GameSortingMapGenerator(object):

    GENRE = "genre"
    RELATIVE_PATH = "path"
    ROOT = "root"

    def __init__(self, gamelist_path, is_single_folder):
        self.gamelist_path = gamelist_path
        self.game_parser = GameListParser(gamelist_path)
        self.genre_aliases_generator = GenreAliasesGenerator(gamelist_path, is_single_folder)
        self.game_list = []

    def get_parsed_games(self):
        if not self.game_list:
            self.process_game_map()

        return self.game_list

    def process_game_map(self):

        print("Processing game map for " + self.gamelist_path)
        for file_name in self.game_parser.get_all_files():

            node = self.game_parser.get_game_node_from_game_file(file_name)

            if node is not None:
                self.__process_games_details(node)

        print("Done processing game map for " + self.gamelist_path)

    def __process_games_details(self, node):

        details = {self.GENRE: self.__compute_game_genre(node),
                   self.RELATIVE_PATH: node.get_genre(),
                   self.ROOT: self.gamelist_path}

        self.game_list.append(details)

    def __compute_game_genre(self, node):

        if self.genre_aliases_generator.document_exists():
            return self.genre_aliases_generator.get_game_genre_alias(node)

        return node.get_genre()
