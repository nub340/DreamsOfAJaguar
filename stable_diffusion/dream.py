import replicate
import webbrowser
import requests
import sys
from PIL import Image
import os

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
    webbrowser.open(url)

def dream_new_unit(type):
    if type == 'air': 
        prompt = STABLE_DIFFUSION_PROMPT_AIR 
        init_image = 'stable_diffusion/init_image/bird2.png'
        # mask = 'stable_diffusion/init_image/bird2mask.png'
    else: 
        prompt = STABLE_DIFFUSION_PROMPT_GROUND
        init_image = 'stable_diffusion/init_image/jag.png'
        # mask = 'stable_diffusion/init_image/jagmask.png'
    
    attempts = 0
    while attempts < 3:
        try:
            output = model.predict(
                prompt=prompt,
                width=STABLE_DIFFUSION_WIDTH,
                height=STABLE_DIFFUSION_HEIGHT,
                prompt_strength=STABLE_DIFFUSION_PSTRENGTH,
                num_inference_steps=STABLE_DIFFUSION_ISTEPS,
                guidance_scale=STABLE_DIFFUSION_GSCALE,
                init_image=open(init_image, "rb"))
                #mask=open(mask, "rb"))
            #print(output)
            attempts = 3

        except Exception as e:
            print('Error generating image. Retrying...')
            attempts += 1
            if attempts > 2:
                raise e

    # print(output)
    return output[0]


def main():
    preview_new_unit(sys.argv[1])

if __name__ == '__main__':
    main()