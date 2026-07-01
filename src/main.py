from bs4 import BeautifulSoup as BS
import os
from pathlib import Path

def read_html(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as rf:
        soup = BS(rf, "lxml")
        
        raw_contents = soup.body.div.table.contents
        mods = [item for item in raw_contents if item != "\n"]

        mod_dict = {}
        for i, mod_row in enumerate(mods):
            mod_td = mod_row.td
            name = mod_td.get_text().strip()
            mod_dict[name] = [name, i, mod_row]

        return mod_dict

def combine_modlists(input_dir: Path, root_dir: Path):
    files = list(input_dir.glob("*.html"))
    if not files:
        return

    files_data = [read_html(f) for f in files]
    
    combined_mod_dict = {}
    for d in files_data:
        combined_mod_dict.update(d)

    # Template is in the same directory as this script (src/)
    template_path = Path(__file__).parent / "Arma 3 Preset combined mods.html"
    
    if not template_path.exists():
        return

    with open(template_path, "r", encoding="utf-8") as rf:
        template = BS(rf, "lxml")

    table = template.body.div.table
    table.clear() 
    for value in combined_mod_dict.values():
        table.append(value[2])

    name_file = input_dir / "mod_list_name.txt"
    if not name_file.exists():
        modlist_name = "Combined"
    else:
        modlist_name = name_file.read_text().strip()

    output_name = f"Arma 3 modlist {modlist_name}.html"
    # Output to the project root (one level up from src/)
    output_path = root_dir / output_name

    with open(output_path, "w", encoding="utf-8") as wf:
        wf.write(str(template))

    with open(output_path, "r", encoding="utf-8") as rf:
        lines = rf.readlines()

    if len(lines) > 78:
        lines[0] = '<?xml version="1.0" encoding="utf-8"?><html>\n'
        lines[2] = "<head>\n"
        lines[4] = f'<meta name="arma:PresetName" content="{modlist_name}" />\n'
        lines[78] = "</style></head><body>\n"

    with open(output_path, "w", encoding="utf-8") as wf:
        wf.writelines(lines)

if __name__ == "__main__":
    # Internal path resolution
    script_path = Path(__file__).resolve()
    # Since main.py is in src/, parent is src/, and parent.parent is root
    root_dir = script_path.parent.parent
    input_path = root_dir / "input"
    
    if input_path.exists():
        combine_modlists(input_path, root_dir)