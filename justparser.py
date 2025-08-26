import json
import re

with open("items_game.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# paint_kits bölümünü ayıkla
paintkits_section = re.search(r'"paint_kits"\s*{(.*?)}\s*}', text, re.DOTALL)
if not paintkits_section:
    raise ValueError("paint_kits bölümü bulunamadı!")

paintkits_text = paintkits_section.group(1)

# paint kit bloklarını yakala: "123" { ... }
pattern = re.compile(r'"(\d+)"\s*{([^}]*)}', re.DOTALL)

paintkits = {}

for match in pattern.finditer(paintkits_text):
    kit_id = match.group(1)
    block = match.group(2)

    # key/value çiftlerini yakala
    kv_pairs = re.findall(r'"([^"]+)"\s+"([^"]+)"', block)
    paintkits[kit_id] = {k: v for k, v in kv_pairs}

with open("paint_kits.json", "w", encoding="utf-8") as f:
    json.dump(paintkits, f, indent=2, ensure_ascii=False)

print(f"{len(paintkits)} paintkit ayrıştırıldı ve paint_kits.json dosyasına yazıldı.")
