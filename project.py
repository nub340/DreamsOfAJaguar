from pickle import FALSE
from game import Game
from stable_diffusion.dream import preview_new_unit
from import_unit import import_all_units, import_unit
from sys import argv
import os

# main game entry point
def main(dream_mode = False):
    game = Game(dream_mode)
    game.run()

# generate and preview new unit by type
def run_preview_unit(type):
    return preview_new_unit(type)

# import all previously generated units
def run_import_units():
    return import_all_units()

# import specific previously generated unit by type and unit number
def run_import_unit(type, unit_no):
    return import_unit(type, unit_no)

if __name__ == '__main__':
    dreaming = False
    
    # check if game is being ran in "dream mode"
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

    # check previewing a new unit
    elif len(argv) > 1 and argv[1] == '-p':
        run_preview_unit(argv[2].strip())
    
    # check if importing
    elif len(argv) > 1 and argv[1] == '-i':
        if len(argv) > 2:
            run_import_unit(argv[2].strip(), argv[3].strip())
        else:
            run_import_units()
    else:
        # run game
        main()
