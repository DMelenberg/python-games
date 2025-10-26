"""
Generate high-quality textures for the 2048 game.
Creates gradient tiles with shadows, highlights, and subtle patterns.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

def create_gradient(width, height, color_top, color_bottom):
    """Create a vertical gradient."""
    base = Image.new('RGB', (width, height), color_top)
    gradient = Image.new('RGB', (width, height), color_bottom)
    
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * y / height)] * width)
    mask.putdata(mask_data)
    
    base.paste(gradient, (0, 0), mask)
    return base

def add_inner_shadow(img, offset=5, blur=10):
    """Add inner shadow to the image."""
    width, height = img.size
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    # Draw shadow rectangle
    draw.rectangle(
        [(offset, offset), (width - offset, height - offset)],
        fill=(0, 0, 0, 60)
    )
    
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    
    # Convert original to RGBA
    img_rgba = img.convert('RGBA')
    img_rgba.paste(shadow, (0, 0), shadow)
    
    return img_rgba

def add_highlight(img, intensity=40):
    """Add a subtle highlight/shine effect."""
    width, height = img.size
    highlight = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(highlight)
    
    # Top highlight
    for i in range(height // 3):
        alpha = int(intensity * (1 - i / (height / 3)))
        draw.rectangle([(0, i), (width, i + 1)], fill=(255, 255, 255, alpha))
    
    img_rgba = img.convert('RGBA')
    return Image.alpha_composite(img_rgba, highlight)

def add_texture_pattern(img, pattern_intensity=15):
    """Add subtle texture pattern."""
    width, height = img.size
    texture = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)
    
    # Add subtle diagonal lines
    for i in range(0, width + height, 4):
        alpha = pattern_intensity
        draw.line([(i, 0), (0, i)], fill=(255, 255, 255, alpha), width=1)
    
    img_rgba = img.convert('RGBA')
    return Image.alpha_composite(img_rgba, texture)

def create_tile(size, color_top, color_bottom, border_radius=10):
    """Create a beautiful tile with gradient, shadow, and highlights."""
    # Create gradient base
    tile = create_gradient(size, size, color_top, color_bottom)
    
    # Add rounded corners
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size, size)], radius=border_radius, fill=255)
    
    tile_rgba = tile.convert('RGBA')
    tile_rgba.putalpha(mask)
    
    # Add effects
    tile_rgba = add_inner_shadow(tile_rgba, offset=3, blur=8)
    tile_rgba = add_highlight(tile_rgba, intensity=35)
    tile_rgba = add_texture_pattern(tile_rgba, pattern_intensity=12)
    
    return tile_rgba

def create_background(width, height):
    """Create a textured background."""
    bg = create_gradient(width, height, (139, 126, 116), (187, 173, 160))
    bg_rgba = bg.convert('RGBA')
    
    # Add subtle pattern
    texture = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)
    
    # Grid pattern
    for i in range(0, width, 20):
        draw.line([(i, 0), (i, height)], fill=(255, 255, 255, 5), width=1)
    for i in range(0, height, 20):
        draw.line([(0, i), (width, i)], fill=(255, 255, 255, 5), width=1)
    
    bg_rgba = Image.alpha_composite(bg_rgba, texture)
    return bg_rgba

def main():
    textures_dir = os.path.dirname(__file__) + '/textures'
    os.makedirs(textures_dir, exist_ok=True)
    
    print("Generating textures...")
    
    # Tile size
    tile_size = 256  # High resolution for quality
    
    # Color schemes for tiles (top, bottom) - more vibrant and appealing
    tile_colors = {
        0: ((210, 198, 186), (204, 192, 179)),      # Empty - beige
        2: ((248, 238, 228), (238, 228, 218)),      # Light cream
        4: ((247, 234, 210), (237, 224, 200)),      # Cream
        8: ((252, 187, 131), (242, 177, 121)),      # Orange
        16: ((255, 159, 109), (245, 149, 99)),      # Dark orange
        32: ((255, 134, 105), (246, 124, 95)),      # Red orange
        64: ((255, 104, 69), (246, 94, 59)),        # Red
        128: ((247, 217, 124), (237, 207, 114)),    # Gold
        256: ((247, 214, 107), (237, 204, 97)),     # Bright gold
        512: ((247, 210, 90), (237, 200, 80)),      # Yellow gold
        1024: ((247, 207, 73), (237, 197, 63)),     # Bright yellow
        2048: ((247, 204, 56), (237, 194, 46)),     # Golden yellow
    }
    
    for value, (color_top, color_bottom) in tile_colors.items():
        tile = create_tile(tile_size, color_top, color_bottom)
        filename = f'{textures_dir}/tile_{value}.png'
        tile.save(filename, 'PNG')
        print(f"✓ tile_{value}.png")
    
    # Create background texture
    bg = create_background(512, 512)
    bg.save(f'{textures_dir}/background.png', 'PNG')
    print("✓ background.png")
    
    print("\nAll textures generated successfully!")

if __name__ == "__main__":
    main()
