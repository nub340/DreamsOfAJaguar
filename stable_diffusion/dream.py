import replicate
import webbrowser
import requests
import sys
from PIL import Image
import os
import csv
from random import choice
from stable_diffusion.unit_request import UnitRequest

# We are mixing image input and prompt input to create unique units. 
# Mask feature is disabled because you get unwanted rigidity. 
# With some more knowledge I beleve the mask layer can be leveraged for unit traits & levels.

# CONFIG ====================
STABLE_DIFFUSION_PROMPT_GROUND = " 16bit Colorful Neon stripes Large Cat , striped tiger orange , stripes , booleans , ints , fangs , cat with spots Running Animation Drawing , detailed drawing , 16 bit video game , cat walking cycle animation sheet , animation drawing sheet , walking cat animation sheet , detailed linework , replicate shape"
STABLE_DIFFUSION_PROMPT_AIR = " pterodactyl , neon color bird , raptor , dinosaur , must have red markings , must have red heads , flapping animation cycle sheet , precisely drawn , 16bit style , detailed drawing , eagle vulture owl , flying animation cycle , mid flight , super sharp talons, claws, side view, mayan art style, Monarobot style, high-definition, sharp lines, catching prey , animation drawing , flying eagle animation sheet , detailed linework , replicate shape"

# ===========================
# Image is a four cell animation sheet  
# Each cell has a frame of animaiton 
# Image must have white background for the alpha layers to work properly
# Animation sheets are all going right so we had to flip the output for the game.
STABLE_DIFFUSION_WIDTH=768
STABLE_DIFFUSION_HEIGHT=768

# ===========================
#PSTRENGTH can be set between .001-1
# (.001-.655) essentially replicates our init_image  
# (.666-.955) returns more unpredictable results 
# (.966-1) returns unique units not speifically following the init_image 
STABLE_DIFFUSION_PSTRENGTH=.777 

# ===========================
#ISTEPS can be set between 1-250
# Higher numbers take longer to process / not specifically better resuts
# 100 Below seems to get less unique results
# 160 Can get great results and then poor results. 
# 200 Seems to return better consistant unique results 
STABLE_DIFFUSION_ISTEPS=200 

# ===========================
#GSCALE can be set between 1-20
# 1-10 will follow init_image more 
# 10-20 returns more unique units
STABLE_DIFFUSION_GSCALE=16 

# ===========================

model = replicate.models.get("stability-ai/stable-diffusion")
unit_requests = []

def get_creature_requests():
    try:
        if not unit_requests or len(unit_requests) == 0:
            with open('stable_diffusion/unit_requests.csv') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    unit_requests.append(UnitRequest(row[0], row[1], row[2], row[3]))
                csvFile.close()
    finally:
        return unit_requests


def ensure_api_key():
    if not os.environ.get('REPLICATE_API_TOKEN'):
        os.environ["REPLICATE_API_TOKEN"] = input('Enter your REPLICATE_API_TOKEN: ').strip()

def clear_dream_dirs():
    dir = 'stable_diffusion/air'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'stable_diffusion/ground'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def regenerate_unit(type, unit_no):
    path = f'stable_diffusion/{type}/{unit_no}.png'
    generate_unit_image(type).save(path)
    return path

def generate_unit_image(type):
    url = dream_new_unit(type)
    return Image.open(requests.get(url, stream=True).raw)

def preview_new_unit(type):
    url = dream_new_unit(type)
    print(url)
    return webbrowser.open(url)

def dream_new_unit(type):
    pool = []
    for unit_req in get_creature_requests():
        if unit_req.unit_type == type:
            pool.append(unit_req)
    unit_request = choice(pool)
    return unit_request.get()

def dream_new_unit_by_name(name):
    pool = list(filter(lambda r: r.name == name, get_creature_requests()))
    unit_request = choice(pool)
    return unit_request.get()

def main():
    preview_new_unit(sys.argv[1])

if __name__ == '__main__':
    main()