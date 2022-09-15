from game import Game
from sys import argv
import os

def main(dream_mode):
    
    game = Game(dream_mode)
    game.run()

if __name__ == '__main__':
    dreaming = False
    if len(argv) > 1 and (argv[1] == '--dream' or argv[1] == '-d'):
        if len(argv) > 2 and argv[2].strip():
            os.environ["REPLICATE_API_TOKEN"] = argv[2].strip()

        dreaming = "REPLICATE_API_TOKEN" in os.environ and len(os.environ["REPLICATE_API_TOKEN"])
        if not dreaming:
            print('\nREPLICATE_API_TOKEN not found. Dream mode requires a token. Falling back to Regular Mode...')
            print('\nYou can either set your token in your ENV first, like this:\n')
            print('\texport REPLICATE_API_TOKEN=<api_token>')
            print('\tpython project.py -dream')
            print('\nor directly in the command line like so:\n\n')
            print('\tpython project.py -dream <api_token>')

    main(dreaming)
