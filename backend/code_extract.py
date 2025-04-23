# Author: Sergej Gorochow

import os
import glob
from datetime import datetime

def extract_files_content_to_txt(directory=os.getcwd(), use_relative_paths=True):
    # Aktuelles Datum für den Dateinamen
    date_str = datetime.now().strftime("%y%m%d_%H%M%S")
    output_filename = f"code_extract_{date_str}.txt"

    # Unterstützte Dateiendungen
    extensions = ['*.vue', '*.js', '*.py', '*.php', '*.go', '*.yml', '*.yaml', '*.html', '*.htm', '*.css', '*.java', '*.class', '*.c', '*.cpp', '*.h', '*.hpp', '*.jsx']
    # Auszuschließende Ordner
    excluded_dirs = {'node_modules', 'venv', 'dist', 'src/assets', 'vendors', }

    # Auszuschließende Dateien
    excluded_files = {'.gitignore', 'code_extract.py'}

    # Basispfad, um relative Pfade zu berechnen
    script_directory = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(script_directory) if use_relative_paths else ''

    # Pfad zur Ausgabedatei im selben Verzeichnis wie das Skript
    output_file_path = os.path.join(script_directory, output_filename)

    with open(output_file_path, 'w', encoding='utf-8') as output:
        # Durchlaufen aller Unterordner
        for root, dirs, files in os.walk(directory):
            # Überprüfen, ob der aktuelle Ordner ausgeschlossen werden sollte
            if any(excluded_dir in root for excluded_dir in excluded_dirs):
                continue

            for extension in extensions:
                # Finden aller Dateien mit der aktuellen Erweiterung
                for filename in glob.glob(os.path.join(root, extension)):
                    # Überprüfen, ob die Datei ausgeschlossen werden sollte
                    if os.path.basename(filename) in excluded_files:
                        continue

                    # Berechnen des relativen oder absoluten Pfads
                    if use_relative_paths:
                        relative_path = os.path.relpath(filename, base_path)
                        output.write(f"Dateiname: {relative_path}\n")
                    else:
                        output.write(f"Dateiname: {filename}\n")

                    # Lesen und Schreiben des Dateiinhalts
                    with open(filename, 'r', encoding='utf-8') as file:
                        output.write(file.read())
                        output.write("\n\n\n")  # Fügt zwei Leerzeilen zwischen den Dateiinhalten hinzu

# Verwenden Sie diese Funktion, um den Prozess zu starten, optionale Pfadangabe, ansonsten im Ordner wo das Skript ist
extract_files_content_to_txt()
