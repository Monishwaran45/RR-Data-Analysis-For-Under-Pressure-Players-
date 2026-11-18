import re, os

path = r'c:\Users\Asus-2025\Downloads\RR\Rajasthan_Royals_SupeRR_Selector_Dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("New dashboard size:", len(text), "bytes")

# Check required section IDs
required_ids = [
    'content-overview', 'content-formulas', 'content-batters', 'content-bowlers',
    'content-tactical', 'content-stability', 'content-simulator', 'content-charts'
]

for rid in required_ids:
    found = f'id="{rid}"' in text
    print(f"ID {rid}: {'OK' if found else 'MISSING'}")

# Check all images exist on disk
images = re.findall(r'<img[^>]*src=[\'"]([^\'"]+)[\'"]', text)
print(f"Total images referenced: {len(images)}")
missing_images = []
for img in images:
    full_path = os.path.join(r'c:\Users\Asus-2025\Downloads\RR', img.replace('/', os.sep))
    if not os.path.exists(full_path):
        missing_images.append(img)

if missing_images:
    print("MISSING IMAGES:", missing_images)
else:
    print("ALL IMAGES EXIST ON DISK! (0 broken paths)")

# Check 5-Year mentions
count_5y = len(re.findall(r'5-Year|Longitudinal', text, re.IGNORECASE))
print(f"5-Year / Longitudinal occurrences: {count_5y}")
