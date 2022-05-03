def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # die 3 Dateien
    count = 0                                                                                   # Zähler für das '\n' Newline Symbol

    for item in filepaths:                      # Iteriere durch die Liste
        with open(item, "r") as f:              # Öffne jedes Listen-Element im Lese-Modus
            count += f.read().count("\n")       # Lese das ganze Dokument, zähle die '\n’, und addiere es

    print("{}".format(count))

if __name__ == "__main__":                      # analog wie in countEntries.py
    main()                                      # man könnte countEntries.py und countLines.py damit zusammen in ein beliebiges anderes Program einbinden
