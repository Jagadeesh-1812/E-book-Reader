from PIL import Image, ImageDraw
import os
import math

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

def create_material_icon(name, color="#FFFFFF", size=64, bg_color=(0, 0, 0, 0)):
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = size // 3
    stroke = size // 10

    if name == 'play':
        points = [
            (center - radius // 2, center - radius),
            (center + radius, center),
            (center - radius // 2, center + radius)
        ]
        draw.polygon(points, fill=color)

    elif name == 'pause':
        bar_width = size // 6
        spacing = size // 10
        draw.rectangle([center - spacing - bar_width, center - radius,
                        center - spacing, center + radius], fill=color)
        draw.rectangle([center + spacing, center - radius,
                        center + spacing + bar_width, center + radius], fill=color)

    elif name == 'stop':
        draw.rectangle([center - radius, center - radius,
                        center + radius, center + radius], fill=color)

    elif name == 'open':
        folder_w = size * 0.65
        folder_h = size * 0.4
        tab_h = size * 0.15
        x = center - folder_w / 2
        y = center - folder_h / 2

        # Folder body
        draw.rectangle([x, y + tab_h, x + folder_w, y + folder_h + tab_h], fill=color)
        # Tab
        draw.rectangle([x + folder_w * 0.1, y, x + folder_w * 0.6, y + tab_h], fill=color)

    elif name == 'settings':
        # Gear-like minimal effect
        for i in range(6):
            angle = math.radians(i * 60)
            x1 = center + math.cos(angle) * (radius + stroke)
            y1 = center + math.sin(angle) * (radius + stroke)
            x2 = center + math.cos(angle) * (radius + stroke * 1.5)
            y2 = center + math.sin(angle) * (radius + stroke * 1.5)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=stroke // 2)

        # Inner circle
        draw.ellipse([center - radius // 2, center - radius // 2,
                      center + radius // 2, center + radius // 2], fill=color)

    img.save(f'images/{name}.png', 'PNG', quality=100)

# Generate all icons at multiple sizes
icons = ['play', 'pause', 'stop', 'open', 'settings']
for icon in icons:
    create_material_icon(icon, size=64)
    create_material_icon(icon, size=32)
    create_material_icon(icon, size=24)
