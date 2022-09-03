import replicate
import webbrowser
import requests
import sys
import uuid
from PIL import Image
import os 
sys.path.append(os.path.realpath('../'))
from import_units import process_all_images

STABLE_DIFFUSION_PROMPT_GROUND = "mayan style , spotted black jaguar , 64bit video game , cat walking cycle animation sheet"
STABLE_DIFFUSION_PROMPT_AIR = "eagle bird buzzard flying animation sheet"

model = replicate.models.get("stability-ai/stable-diffusion")

def clear_folder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def refresh_units():
    clear_folder('import_units/air')
    clear_folder('import_units/ground')
    clear_folder('graphics/units/air')
    clear_folder('graphics/units/ground')

    print('dreaming up new units...')
    for _ in range(0, 3):
        generate_unit_image('air').save(f'import_units/air/{uuid.uuid4()}.png')
        generate_unit_image('ground').save(f'import_units/ground/{uuid.uuid4()}.png')
    
    print('\ncomplete! Importing dreamt units...')
    process_all_images()
    print('Dreamt units imported successfully!')
    
def generate_unit_image(type):
    url = generate_unit_url(type)
    return Image.open(requests.get(url, stream=True).raw)

def preview_generated_unit(type):
    output_url = generate_unit_url(type)
    print(output_url)
    webbrowser.open(output_url)

def generate_unit_url(type):
    if type == 'air': 
        prompt = STABLE_DIFFUSION_PROMPT_AIR 
        image = 'stable_diffusion/img2img/bird.png'
    else: 
        prompt = STABLE_DIFFUSION_PROMPT_GROUND
        image = 'stable_diffusion/img2img/jag.png'
    
    attempts = 0
    while attempts < 3:
        try:
            output = model.predict(
                prompt=prompt,
                width=512,
                height=512,
                prompt_strength=0.8,
                num_inference_steps=50,
                guidance_scale=7.5,
                init_image=open(image, "rb"))

            attempts = 3

        except Exception as e:
            print('Error generating image. Retrying...')
            attempts += 1
            if attempts > 2:
                raise e

    print(output)
    return output[0]


def main():
    preview_generated_unit(sys.argv[1])

if __name__ == '__main__':
    main()