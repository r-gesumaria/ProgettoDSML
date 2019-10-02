import xml.etree.ElementTree as ET
import mysql.connector
import sys
import csv
import os

def creaConnessione(nomeDB):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database = nomeDB
    )

def creaDb(tipoSchema):
    # Connessione a mysql e creazione db
    mydb = creaConnessione("")
    mycursor = mydb.cursor()
    nomeDb = tipoSchema + "_" + sys.argv[2]
    # Elimino il db se già esiste
    mycursor.execute("DROP DATABASE IF EXISTS `" + nomeDb + "`;")
    mydb.commit()
    mycursor.execute("CREATE DATABASE " + nomeDb)
    mydb.close

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    table = ""
    # Recupero la parte iniziale
    path = os.path.normpath(sys.argv[1])
    nomeFile = path.split(os.sep)[-1]
    inizioPath = sys.argv[1]
    inizioPath = inizioPath[:(sys.argv[1].__len__() - nomeFile.__len__())]
    print(inizioPath)
    print(nomeFile)

    # Connessione al db appena creato e generazione delle tabelle con attributi
    mydb = creaConnessione(nomeDb)
    mycursor = mydb.cursor()
    for c in root.findall("./Schemas/" + tipoSchema + "/Relation"):
        # Per ogni relazione, conto quanti attributi ci sono
        nAttr = 0
        nameEn = c.get('name')
        table = 'CREATE TABLE ' + nameEn + ' ('

        attributi = root.findall("./Schemas/" + tipoSchema + "/*[@name='" + nameEn + "']/Attr")
        for a in attributi:
            table += a.find('Name').text
            if (a.find('DataType').text == 'TEXT'):
                table += ' varchar(100),'
            elif (a.find('DataType').text == 'INT8'):
                table += ' INT(100),'
            nAttr=nAttr+1

        table = table[:-1]

        # Aggiungo la PK
        pk = root.findall("./Schemas/" + tipoSchema + "/*[@name='" + nameEn + "']/PrimaryKey")
        if(pk is not None):
            table += ", PRIMARY KEY (" + pk[0].find("Attr").text + ")"
        table += ');'
        mycursor.execute(table)
        if(tipoSchema == "SourceSchema"):
            caricaDati(mycursor, inizioPath, nameEn, nAttr)
        mydb.commit()

    # Aggiungo le chiavi esterne alle tabelle
    mycursor = mydb.cursor()
    query = ""
    fks = root.findall("./Schemas/" + tipoSchema + "/ForeignKey")
    for f in fks:
        # Tabella from
        t1 = f.find("From").get("tableref")
        # Campo from
        e1 = f.find("From/Attr").text
        # Tabella to
        t2 = f.find("To").get("tableref")
        # Campo to
        e2 = f.find("To/Attr").text
        query = "ALTER TABLE " + t1 + " ADD FOREIGN KEY (" + e1 + ") REFERENCES " + t2 + "(" + e2 + ");"
        mycursor.execute(query)
    mydb.commit()

def caricaDati(cursor, path, nomeEntita, numeroAttributi):
    '''
        NOTA: Esiste un csv per ogni entità
    '''
    queryRiga = ""
    with open(path + nomeEntita + ".csv", 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        for row in csv_data:
            queryRiga = 'INSERT INTO ' + nomeEntita + ' VALUES('
            # I valori sono separati da una pipe
            vals = row[0].split("|")
            attributiDaInserire = numeroAttributi
            for v in range(len(vals)):
                if(attributiDaInserire < 1): break
                # Il primo è il numero della riga di excel
                if(v==0):continue
                # Concateno il valore della cella
                queryRiga += "'" + vals[v].replace("'"," ") + "',"
                attributiDaInserire = attributiDaInserire-1
            # Tolgo l'ultima virgola
            queryRiga = queryRiga[:-1]
            queryRiga += ")"
            cursor.execute(queryRiga)

if((sys.argv.__len__()) != 3):
    print("Uso: nomeScript nomeFile/pathFile nomeDb")
else:
    creaDb("SourceSchema")
    creaDb("TargetSchema")