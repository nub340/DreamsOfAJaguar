from game import Game
from sys import argv
import os

from import_unit import regenerate_all_units, import_all_units

def main(dream_mode):
    
    # if dream_mode:
    #     regenerate_all_units()
    #     import_all_units()

    game = Game(dream_mode)
    game.run()

if __name__ == '__main__':
    if len(argv) > 1 and (argv[1] == '--dream' or argv[1] == '-d'):
        if len(argv) > 2 and argv[2]:
            os.environ["REPLICATE_API_TOKEN"] = argv[2].strip()

        main(True)
    else:
        main(False)
    
