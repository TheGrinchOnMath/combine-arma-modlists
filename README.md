## Arma Modlist combination tool.
the objective of this project is to take several arma 3 modlist html files, combine them and return a single HTML file containing all mods from the other files.

## Setup:
### For windows users:
run `python.exe -m venv .env`
- for windows 10 cmd, run `.env\Scripts\activate.bat`
- for powershell, run `.env\Scripts\Activate.ps1`
- for windows 11 terminal, run `.env\Scripts\activate`
then, run `pip install -r requirements.txt`. this should install the necessary library. 

## Usage instructions:
- export all the modlists you want to combine
- place all of the generated files in the folder named input
- edit the text in mod_list_name.txt to the name of the combined mod list. 
`important: do not use any special characters (the text will be used to name the output file, so respect file naming conventions and limitations)`

- run the python file called `main.py`