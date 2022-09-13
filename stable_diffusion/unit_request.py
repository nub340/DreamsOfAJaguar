import replicate

class UnitRequest():
    def __init__(self, name, unit_type, prompt, init_image, prompt_strength=.777, width=768, height=768, num_inference_steps=200, guidance_scale=16, mask = None, seed = None, model = "stability-ai/stable-diffusion"):
        self.model = replicate.models.get(model)
        self.name = name
        self.unit_type = unit_type
        self.prompt = prompt
        self.prompt_strength = prompt_strength
        self.width = width
        self.height = height
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self.init_image = init_image
        self.mask = mask
        self.seed = seed

    def get(self):
        attempts = 0
        while attempts < 3:
            try:
                print(f'Requesting new {self.name}')
                output = self.model.predict(
                    prompt=self.prompt,
                    width=self.width,
                    height=self.height,
                    prompt_strength=self.prompt_strength,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=self.guidance_scale,
                    init_image=open(self.init_image, "rb"))
                    #mask=open(mask, "rb"))

                attempts = 3

            except Exception as e:
                print('Error generating image. Retrying...')
                attempts += 1
                if attempts > 2:
                    raise e

        # return url to generated image
        return output[0]