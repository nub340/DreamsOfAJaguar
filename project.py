from game import Game
from sys import argv

from unit_factory import regenerate_all_units, import_all_units

def main(dream):
    
    if dream:
        regenerate_all_units()
        import_all_units()

    game = Game()
    game.run()

if __name__ == '__main__':
    if len(argv) > 1 and (argv[1] == '--dream' or argv[1] == '-d'):
        main(True)
    else:
        main(False)
    
