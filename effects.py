import pygame 
from PIL import Image, ImageFilter

def make_dreamy(input_surf, color = (255, 255, 255), border_width = 2, blur_radius = None):
        
        # create mask surface from mask of input_surf, set black pixels to be transparent
        input_mask_surf = pygame.mask.from_surface(input_surf).to_surface().convert()
        input_mask_surf.set_colorkey((0,0,0))

        # change color of all non-black pixels
        input_w, input_h = input_mask_surf.get_size()
        for x in range(input_w):
            for y in range(input_h):
                if input_mask_surf.get_at((x, y))[0] != 0:
                    input_mask_surf.set_at((x, y), color)

        # calculate some needed dimensions. Square the blur radius to avoid clipping.
        if blur_radius:
            padding = (border_width * blur_radius)
            output_w = input_w + (padding * 2) + (blur_radius**2)
            output_h = input_h + (padding * 2) + (blur_radius**2)
        else:
            padding = (border_width)
            output_w = input_w + (padding * 2) 
            output_h = input_h + (padding * 2)

        # draw border/background...
        # blit mask surface 9 times, each offset in a different direction relative to the center: 
        # topleft, left, bottomleft, up, center, down, topright, right, bottomright. 
        input_mask_centered_rect = input_mask_surf.get_rect(center = (output_w/2, output_h/2))
        output_surface = pygame.Surface((output_w, output_h), pygame.SRCALPHA).convert_alpha()
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y+padding))

        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y+padding))

        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y+padding))

        # blur the resulting border/background via PIL and then convert it back to a surface
        if blur_radius:
            image = Image.frombytes(
                "RGBA", 
                output_surface.get_size(), 
                pygame.image.tostring(output_surface, 'RGBA')).filter(
                    ImageFilter.GaussianBlur(blur_radius))

            output_surface = pygame.image.fromstring(
                image.tobytes("raw", 'RGBA'), 
                output_surface.get_size(), 
                'RGBA')

        # finally, blit the original unaltered input surface centered onto the output_surface
        output_surface.blit(input_surf, input_surf.get_rect(center = (output_w/2, output_h/2)))
        return output_surface