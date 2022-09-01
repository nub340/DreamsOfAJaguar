from game import Game
from sys import argv

def main(dream):
    game = Game()
    game.run(dream)

if __name__ == '__main__':
    if len(argv) > 1 and (argv[1] == '--dream' or argv[1] == '-d'):
        main(True)
    else:
        main(False)
    
