import json
import re

# items_game.txt dosyasını aç
with open("items_game.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# paint_kits bölümünü yakala
paintkits_section = re.search(r'"paint_kits"\s*{([\s\S]*?)}\s*}', text, re.DOTALL)
if not paintkits_section:
    raise ValueError("paint_kits bölümü bulunamadı!")

paintkits_text = paintkits_section.group(1)

# paintkit bloklarını yakala
pattern = re.compile(r'"(\d+)"\s*{([^}]*)}', re.DOTALL)

paintkits = {}
base_url = "http://media.steampowered.com/apps/730/icons/econ/default_generated"

for match in pattern.finditer(paintkits_text):
    kit_id = match.group(1)
    block = match.group(2)
    kv_pairs = dict(re.findall(r'"([^"]+)"\s+"([^"]+)"', block))

    internal_name = kv_pairs.get("name", None)
    if internal_name:
        # URL oluştur
        url = f"{base_url}/{internal_name}_light_large.png"
        kv_pairs["image_url"] = url

    paintkits[kit_id] = kv_pairs

# Sonucu JSON dosyasına yaz
with open("paint_kits_with_urls.json", "w", encoding="utf-8") as f:
    json.dump(paintkits, f, indent=2, ensure_ascii=False)

print(f"{len(paintkits)} paintkit ayrıştırıldı ve paint_kits_with_urls.json dosyasına yazıldı ✅")
