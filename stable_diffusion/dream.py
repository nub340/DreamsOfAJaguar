import replicate
import webbrowser
import requests
import sys
from PIL import Image
import os

# CONFIG ====================
STABLE_DIFFUSION_PROMPT_GROUND = "facing left , Saber-toothed cat , detailed drawing , 32bit video game , cat walking cycle animation sheet"
STABLE_DIFFUSION_PROMPT_AIR = "precisely drawn illustration, 4k, drawing of 4 colorful quetzal bird eagle vulture animals, identical, facing left, flying through the air, mid flight, super sharp talons, claws, side view, mayan art style, Monarobot style, high-definition, sharp lines, catching prey"
STABLE_DIFFUSION_WIDTH=768
STABLE_DIFFUSION_HEIGHT=768
STABLE_DIFFUSION_PSTRENGTH=0.8
STABLE_DIFFUSION_ISTEPS=50
STABLE_DIFFUSION_GSCALE=7.5
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
        init_image = 'stable_diffusion/init_image/bat.png'
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