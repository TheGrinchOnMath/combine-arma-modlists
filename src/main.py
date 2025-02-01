#
from bs4 import BeautifulSoup as BS
import os
from contextlib import chdir


# function: read a html file, extract mods etc
def read_html(PATH: str) -> dict:
    # open file, read file, parse file
    with open(PATH, "r") as rf:
        soup = BS(rf, "lxml")
        # ---- Parse Mods ---- #

        # extract mod list div, get the children of the mods file as a table
        mods = soup.body.div.table.contents

        # remove newlines that have popped up due to formatting
        for mod in mods:
            mods.remove("\n")

        # create dictionary of mods, containing name, html & index
        mod_dict = {}
        for i in range(len(mods)):
            mod = mods[i].td

            # remove excess \n\t tags (credit: "https://stackoverflow.com/a/3939381")
            name = mod.contents[0].translate({ord(c): None for c in "\n\t"})

            # create dict for each mod
            mod_data = [name, i, mods[i]]
            mod_dict[name] = mod_data

        return mod_dict
        # -------------------- #


def combine_modlists(input_dir: str):
    # parse dir, get html files
    files = []
    # magic by
    # list files in dir
    for filename in os.listdir(input_dir):
        file = os.path.join(input_dir, filename)
        _, ext = os.path.splitext(file)
        if os.path.isfile(file) and ext == ".html":
            files.append(file)

    files_data = []

    # read all files, collect dicts
    for file_path in files:
        data = read_html(file_path)
        files_data.append(data)

    temp_list = files_data[1:]
    mod_dict = files_data[0]

    # compare dictionaries and fuse them
    for _dict in temp_list:
        mod_dict.update(_dict)

    # now we have to create a new modlist using the dict.
    # copy the template html file to output
    with open(
        os.path.join(os.getcwd(), "src", "Arma 3 Preset combined mods.html"), "r"
    ) as rf:
        template = BS(rf, "lxml")

    # create a list of mod html snippets
    html_snippets = []
    for _, value in mod_dict.items():
        html_snippets.append(value[2])

    # replace the modlist mods div with the combined mods
    for snippet in html_snippets:
        template.body.div.table.append(snippet)

    # get the desired name for the modlist
    with open(os.path.join(os.getcwd(), "input", "mod_list_name.txt")) as rf:
        modlist_name = rf.read()
        file_name = f"Arma 3 modlist {modlist_name}.html"

    # write to file
    with open(file_name, "w") as wf:
        wf.write(str(template))

    # cant be bothered to actually fix the parsing of the head of the file, so we are modding 3 lines to conform to the original structure.
    with open(file_name, "r") as file:
        lines = file.readlines()
        lines[0] = '<?xml version="1.0" encoding="utf-8"?><html>'
        lines[2] = "<head>"
        lines[4] = f'<meta name="arma:PresetName" content="{modlist_name}" />'
        lines[78] = "</style></head><body>"

    with open(file_name, "w") as file:
        file.writelines(lines)

    # get dictionary for each file, inside a list for convenience


# check if in src directory cuz doofus users
CWD = os.getcwd()
full_CWD = CWD.split(os.path.sep)
if full_CWD[-1] == "src":
    with chdir(".."):
        path = os.path.join(os.getcwd(), "input")

        combine_modlists(path)
else:
    path = os.path.join(os.getcwd(), "input")

    combine_modlists(path)
