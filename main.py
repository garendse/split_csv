import PySimpleGUI as sg
import pandas as pd
import os
import shutil

gchunk_size=5000
gprefix="part_"

# Clear generated files
def _clean_files() -> None:
    print("Cleaning data")
    try:
        with os.scandir("split") as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                else:
                    os.remove(entry.path)

    except Exception as e:
        print(e)


def _split_csv_file(csv_file: str, chunk_size: int) -> None:
    try:
        for i, chunk in enumerate(pd.read_csv(csv_file, sep='|', chunksize=chunk_size, header=1)):
            print(f"Writing chunk {i}")
            chunk.to_csv("split/" + gprefix + "-" + str(i) + ".csv", index=False, sep='|', na_rep="", header=False)

    except pd.errors.EmptyDataError:
        print("No data in file: " + csv_file)

def _get_csv_filename() -> str:
    global gprefix
    global gchunk_size

    layout = [
        [sg.Text("CSV Data File: "), sg.Input(), sg.FileBrowse(key="-CSV-", file_types=(("CSV Files", "*.csv"),))],
        [sg.Text("Chunk Prefix: "), sg.Input(key='-CKP-', size=(6, 1), default_text=f"{gprefix}")],
        [sg.Text("Chunk Size: "), sg.Input(key='-CKN-', size=(6, 1), default_text=f"{gchunk_size}")],
        [sg.Button("Submit"), sg.Cancel()]]

    window = sg.Window("CSV File Splitter", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Submit":
            gchunk_size = int(values['-CKN-'])
            gprefix = values['-CKP-']
            return values["-CSV-"]


if __name__ == '__main__':
    csv_fname = _get_csv_filename()

    if len(csv_fname) > 0:
        try:
            _clean_files()

            print("Reading", csv_fname)
            _split_csv_file(csv_fname, gchunk_size)
            print("Done")

        except Exception as e:
            print("Error:", e)