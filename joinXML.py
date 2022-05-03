def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]             # die 3 zerteilten XML Dateien
    destination = "mkg_lido-dC.web.xml"                                                                 # Ziel für eine zusammengeführte Datei

    data = []                                   # Leere Liste für die Inhalte der 3 Dateien

    for item in filepaths:                      # Iteriere durch die 3 Dateien
        with open(item, "r") as f:              # Öffne 1 im Lese-Modus
            data.append(f.read())               # Lese die ganze Datei und hänge es als neues Element an die data Liste an
        print("Joined {}".format(item))


    data = "\n\n".join(data)                # Schmelze die 3 Listen zu einem String zusammen mit einem '\n\n' dazwischen. Bad style though.
    with open(destination, "w") as f:       # Öffne die Ziel-Datei im Schreib-Modus, überschreibt sie wenn sie schon existiert, zum hinten anfügen ohne löschen "a"
        f.write(data)                       # Schreibe den gesamten verschmolzenen Text dort rein


if __name__ == "__main__":                  # analog zu countEntries.py und countLines.py
    main()



# Python arbeitet nicht mit {} sondern mit indentation, also whitespace am Anfang der Zeile.
# Das muss "auf dem gleichen Level" immer genau gleich viel sein. Standardmäßig 4 Leerzeichen.
# Tabs funktionieren auch, aber nie Leerzeichen und Tabs zusammen da 1 Tab != 4 Leerzeichen.


# Die beiden Code-Snippets sind äquivalent, aber die erste ist mehr "pythonic" und allgemein bevorzugt

#   with open(path, "r") as f:
#       content = f.read()

#   f = open(path, "r")
#   content = f.read()
#   f.close()
