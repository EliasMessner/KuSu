def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # Liste der 3 Dateipfade
    count_open = 0                                                                              # Zähler für öffnende <lido:lido> Tags, für alle 3 Dateien zusammen
    count_close = 0                                                                             # Zähler für schließende Tags, zur Kontrolle

    for item in filepaths:                                  # iteriere durch die Liste, item ist erst eine Kopie von filepaths[0] dann von filepaths[1] usw
        with open(item, "r") as f:                          # öffne eine Datei im Lese-Modus
            data = f.read()                                 # lese die ganze Datei und speichere den Inhalt in data
            count_open += data.count("<lido:lido>")         # zähle die Anzahl dieses tags in dieser 1 Datei und addiere es zum gesamten
            count_close += data.count("</lido:lido>")

    print("{}\n{}".format(count_open, count_close))


if __name__ == "__main__":              # wenn man dieses Programm in einem anderem Programm einfügt wird der Code dort durch diese 2 Zeilen nicht sofort ausgeführt
    main()                              # man würde dann in dem anderen Program sowas wie "import countEntries" eingeben und dann "countEntries.main()" ausführen
