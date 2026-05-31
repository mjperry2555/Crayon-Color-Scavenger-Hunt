# Crayons Scavenger Hunt
# Perceptual Color Matching

import ui, photos, console, math, json, os, io
from PIL import Image

# For best results:
# 1. Photograph under natural light
# 2. Avoid shadows
# 3. Fill frame with colors

# --- Settings & Data ---
SAVE_FILE = os.path.expanduser('~/Documents/crayola_found.json')

PALETTE = {
    # Reds / Pinks
    "Red": (238, 32, 77), "Scarlet": (252, 40, 71), "Maroon": (200, 56, 90),
    "Brick Red": (203, 65, 84), "Red-Orange": (255, 83, 73), "Orange Red": (255, 43, 43),
    "Magenta": (246, 83, 166), "Red-Violet": (192, 68, 143), "Wild Strawberry": (255, 67, 164),
    "Pink": (255, 192, 203), "Carnation Pink": (255, 170, 204), "Tickle Me Pink": (252, 137, 172),
    "Melon": (253, 188, 180), "Pink Sherbet": (247, 143, 167), "Shocking Pink": (255, 110, 199),
    "Razzmatazz": (227, 37, 107), "Mulberry": (197, 75, 140), "Orchid": (230, 168, 215),
    "Lavender": (252, 180, 213), "Thistle": (235, 199, 223), "Magic Potion": (255, 68, 10),
    "Pink Flamingo": (252, 116, 253), "Hot Magenta": (255, 29, 206), "Purple Pizzazz": (255, 29, 206),
    "Razzle Dazzle Rose": (255, 72, 208), "Eggplant": (110, 81, 96), "Cerise": (221, 68, 146),
    "Cotton Candy": (255, 188, 217), "Piggy Pink": (253, 215, 228), "Jazzberry Jam": (202, 55, 103),
    "Blush": (222, 93, 131), "Radical Red": (255, 73, 108), "Mauvelous": (239, 152, 170),
    "Wild Watermelon": (252, 108, 133), "Salmon": (255, 155, 170), "Timberwolf": (219, 215, 210),

    # Oranges / Yellows
    "Orange": (255, 117, 56), "Burnt Orange": (255, 127, 73), "Neon Carrot": (255, 163, 67),
    "Macaroni and Cheese": (255, 189, 136), "Yellow-Orange": (255, 174, 66), "Goldenrod": (252, 217, 117),
    "Dandelion": (253, 219, 109), "Yellow": (252, 232, 131), "Laser Lemon": (254, 254, 34),
    "Unmellow Yellow": (255, 255, 102), "Electric Lime": (204, 255, 0), "Green-Yellow": (240, 232, 145),
    "Spring Green": (236, 234, 190), "Yellow-Green": (197, 227, 132), "Olive Green": (186, 184, 108),
    "Moss Green": (138, 154, 91), "Canary": (255, 255, 159), "Sunglow": (255, 207, 72),
    "Atomic Tangerine": (255, 164, 116), "Smashed Pumpkin": (255, 109, 58), "Sunset Orange": (253, 94, 83),
    "Bittersweet": (253, 124, 110), "Outrageous Orange": (255, 110, 74), "Vivid Tangerine": (255, 160, 137),
    "Violet Red": (247, 83, 148), "Banana Mania": (250, 231, 181),

    # Greens
    "Green": (28, 172, 120), "Forest Green": (109, 174, 129), "Sea Green": (159, 226, 191),
    "Shamrock": (69, 206, 162), "Jungle Green": (59, 176, 143), "Pine Green": (21, 128, 120),
    "Screamin Green": (118, 255, 122), "Asparagus": (135, 169, 107), "Tropical Rain Forest": (23, 128, 109),
    "Fern": (113, 188, 120), "Caribbean Green": (28, 211, 162), "Mountain Meadow": (48, 186, 143),
    "Granny Smith Apple": (168, 228, 160), "Inchworm": (178, 236, 93),

    # Blues
    "Turquoise Blue": (119, 221, 231), "Aquamarine": (120, 219, 226), "Sky Blue": (128, 218, 235),
    "Pacific Blue": (28, 169, 201), "Cerulean": (29, 172, 214), "Robin's Egg Blue": (31, 206, 203),
    "Blue-Green": (13, 152, 186), "Blue": (31, 117, 254), "Denim": (43, 108, 196),
    "Navy Blue": (25, 116, 210), "Indigo": (93, 118, 203), "Wild Blue Yonder": (162, 173, 208),
    "Shadow Blue": (119, 139, 165), "Bluetiful": (46, 106, 187), "Outer Space": (65, 74, 76),
    "Cornflower": (154, 206, 235), "Midnight Blue": (26, 72, 118), "Periwinkle": (197, 208, 230),
    "Cadet Blue": (176, 183, 198), "Manatee": (151, 154, 170), "Blue Bell": (173, 173, 214),

    # Purples
    "Blue-Violet": (115, 102, 189), "Violet-Blue": (50, 74, 178), "Violet": (146, 110, 174),
    "Purple Heart": (116, 66, 200), "Plum": (142, 69, 133), "Royal Purple": (120, 81, 169),
    "Purple Mountains Majesty": (157, 129, 186), "Wisteria": (205, 164, 222), "Vivid Violet": (143, 80, 157),
    "Fuchsia": (195, 100, 197),

    # Browns / Neutrals
    "Mahogany": (205, 74, 76), "Burnt Sienna": (234, 126, 93), "Raw Sienna": (214, 138, 89),
    "Sepia": (165, 105, 79), "Brown": (180, 103, 77), "Beaver": (159, 129, 112),
    "Desert Sand": (239, 205, 184), "Tan": (250, 167, 108), "Peach": (255, 203, 164),
    "Apricot": (253, 217, 181), "Almond": (239, 222, 205), "Shadow": (138, 121, 93),
    "Antique Brass": (205, 149, 117), "Fuzzy Wuzzy Brown": (204, 102, 102), "Chestnut": (188, 93, 88),

    # Grays / Black / White
    "Black": (35, 35, 35), "Charcoal Gray": (115, 115, 115), "Gray": (149, 145, 140),
    "Gold": (231, 198, 151), "Silver": (205, 197, 194), "Copper": (221, 148, 117),
    "White": (255, 255, 255)
}

def load_found():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                return set(json.load(f))
        except:
            pass
    return set()

found_colors = load_found()

def save_found():
    with open(SAVE_FILE, 'w') as f:
        json.dump(list(found_colors), f)

# --- Perceptual Color Functions ---
def rgb_to_xyz(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    r = r ** 2.4 if r > 0.04045 else r / 12.92
    g = g ** 2.4 if g > 0.04045 else g / 12.92
    b = b ** 2.4 if b > 0.04045 else b / 12.92
    
    r, g, b = r * 100, g * 100, b * 100
    
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    return x, y, z

def xyz_to_lab(x, y, z):
    xr, yr, zr = 95.047, 100.0, 108.883
    x, y, z = x / xr, y / yr, z / zr
    
    def f(t):
        return t ** (1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)
    
    fx, fy, fz = f(x), f(y), f(z)
    l = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return l, a, b

def rgb_to_lab(rgb):
    x, y, z = rgb_to_xyz(rgb)
    return xyz_to_lab(x, y, z)

def ciede2000(lab1, lab2):
    """CIEDE2000 - Significantly more accurate perceptual color difference"""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    Cbar = (C1 + C2) / 2
    
    G = 0.5 * (1 - math.sqrt(Cbar**7 / (Cbar**7 + 25**7)))
    
    a1p = a1 * (1 + G)
    a2p = a2 * (1 + G)
    C1p = math.sqrt(a1p**2 + b1**2)
    C2p = math.sqrt(a2p**2 + b2**2)
    
    h1p = math.atan2(b1, a1p) if C1p != 0 else 0
    h2p = math.atan2(b2, a2p) if C2p != 0 else 0
    
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    if dhp > math.pi: dhp -= 2 * math.pi
    if dhp < -math.pi: dhp += 2 * math.pi
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(dhp / 2)
    
    Lbarp = (L1 + L2) / 2
    Cbarp = (C1p + C2p) / 2
    hbarp = h1p + h2p
    if abs(h1p - h2p) > math.pi:
        hbarp += math.pi if h1p + h2p < 2*math.pi else -math.pi
    
    T = (1 - 0.17 * math.cos(hbarp - math.pi/6) +
         0.24 * math.cos(2 * hbarp) +
         0.32 * math.cos(3 * hbarp + math.pi/6) -
         0.20 * math.cos(4 * hbarp - 63*math.pi/180))
    
    SL = 1 + (0.015 * (Lbarp - 50)**2) / math.sqrt(20 + (Lbarp - 50)**2)
    SC = 1 + 0.045 * Cbarp
    SH = 1 + 0.015 * Cbarp * T
    
    dtheta = 30 * math.exp(-((hbarp - 275*math.pi/180)/25)**2)
    RC = 2 * math.sqrt(Cbarp**7 / (Cbarp**7 + 25**7))
    RT = -RC * math.sin(2 * dtheta)
    
    return math.sqrt((dLp / SL)**2 + (dCp / SC)**2 + (dHp / SH)**2 + RT * (dCp / SC) * (dHp / SH))

# Pre-compute LAB values
PALETTE_LAB = {name: rgb_to_lab(rgb) for name, rgb in PALETTE.items()}

def closest_color(rgb):
    lab = rgb_to_lab(rgb)
    best_name, best_d = None, 1e9
    for name, lab_val in PALETTE_LAB.items():
        d = ciede2000(lab, lab_val)      # ← Upgraded to CIEDE2000
        if d < best_d:
            best_d, best_name = d, name
    return best_name

def average_color(img, x, y, r=8):
    p = img.load()
    w, h = img.size
    rs = gs = bs = c = 0
    for i in range(max(0, x - r), min(w, x + r + 1)):
        for j in range(max(0, y - r), min(h, y + r + 1)):
            pixel = p[i, j]
            rs += pixel[0]
            gs += pixel[1]
            bs += pixel[2]
            c += 1
    return (rs // c, gs // c, bs // c) if c > 0 else (0, 0, 0)

# --- UI Class ---
class CrayonHunter(ui.View):
    def __init__(self, pil_img, ui_img):
        self.pil_img = pil_img
        self.name = "Crayon Scavenger Hunt"
        
        self.img_view = ui.ImageView(frame=self.bounds, flex='WH')
        self.img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        self.img_view.image = ui_img
        self.add_subview(self.img_view)
        
        self.label = ui.Label(frame=(0, self.height - 90, self.width, 90), flex='WT')
        self.label.background_color = (0, 0, 0, 0.75)
        self.label.text_color = 'white'
        self.label.alignment = ui.ALIGN_CENTER
        self.label.number_of_lines = 3
        self.label.text = f"Tap a crayon!\nFound: {len(found_colors)}/{len(PALETTE)}"
        self.add_subview(self.label)
        
        self.reset_btn = ui.Button(title="Reset", frame=(10, 10, 100, 44))
        self.reset_btn.background_color = (0.8, 0.1, 0.1, 0.9)
        self.reset_btn.tint_color = 'white'
        self.reset_btn.corner_radius = 8
        self.reset_btn.action = self.reset_progress
        self.add_subview(self.reset_btn)

    def reset_progress(self, sender):
        if console.alert("Reset Progress", "Clear all found colors?", "Yes", "Cancel") == 1:
            found_colors.clear()
            save_found()
            self.label.text = f"Progress reset!\n0/{len(PALETTE)}"
            console.hud_alert("Progress Reset", 'error')

    def touch_began(self, touch):
        iw, ih = self.pil_img.size
        vw, vh = self.width, self.height
        
        scale = min(vw / iw, vh / ih)
        ox = (vw - iw * scale) / 2
        oy = (vh - ih * scale) / 2
        
        img_x = int((touch.location.x - ox) / scale)
        img_y = int((touch.location.y - oy) / scale)
        
        if 0 <= img_x < iw and 0 <= img_y < ih:
            rgb = average_color(self.pil_img, img_x, img_y)
            name = closest_color(rgb)
            
            was_new = name not in found_colors
            if was_new:
                found_colors.add(name)
                save_found()
                console.hud_alert(f"🎉 New! {name.upper()}", 'success', 1.5)
            else:
                console.hud_alert(f"{name.upper()}", 'success', 0.8)
            
            self.label.text = f"That's {name.upper()}!\nProgress: {len(found_colors)}/{len(PALETTE)}"
            if was_new:
                self.label.text += "\n🎨 NEW DISCOVERY!"

# --- Entry Point ---
def main():
    console.clear()
    
    picked_object = photos.pick_image(raw_data=True)
    if not picked_object:
        return

    if hasattr(picked_object, 'getvalue'):
        img_bytes = picked_object.getvalue()
    else:
        img_bytes = picked_object

    try:
        buffer = io.BytesIO(img_bytes)
        pil_img = Image.open(buffer).convert('RGB')
        ui_img = ui.Image.from_data(img_bytes)
    except Exception as e:
        print(f"Loading Error: {e}")
        return

    view = CrayonHunter(pil_img, ui_img)
    view.present('fullscreen')

if __name__ == '__main__':
    main()
