import xml.etree.ElementTree as ET
import mysql.connector
import sys
import csv

def creaConnessione(nomeDB):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database = nomeDB
    )

def creaDb(tipoSchema):
    #connessione a mysql e creazione db
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
    path = sys.argv[1]
    path = path.split("/")
    inizioPath = sys.argv[1]
    inizioPath = inizioPath[:len(sys.argv[1])-len(path[-1])]

    #connessione al db appena creato e generazione delle tabelle con attributi
    mydb = creaConnessione(nomeDb)
    mycursor = mydb.cursor()
    for c in root.findall("./Schemas/" + tipoSchema + "/Relation"):
        nameEn = c.get('name')
        table = 'CREATE TABLE ' + nameEn + ' ('

        attributi = root.findall("./Schemas/" + tipoSchema + "/*[@name='" + nameEn + "']/Attr")
        for a in attributi:
            table += a.find('Name').text
            if (a.find('DataType').text == 'TEXT'):
                table += ' varchar(100),'

        table = table[:-1]
        table += ')'
        mycursor.execute(table)
        caricaDati(mycursor, inizioPath, nameEn)
        mydb.commit()

    #print(table)

def caricaDati(cursor, path, nomeEntita):
    '''TODO caricare dati
        Esiste un csv per ogni entità
        Controllare se per il target esiste un csv
        Valutare se creare una cartella a parte stesso da ibench
    '''
    queryRiga = ""
    with open(path + nomeEntita + ".csv", 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        for row in csv_data:
            queryRiga = 'INSERT INTO ' + nomeEntita + ' VALUES('
            # I valori sono separati da una pipe
            vals = row[0].split("|")
            for v in range(len(vals)):
                # Il primo è il numero della riga di excel
                if(v==0):continue
                # Concateno il valore della cella
                queryRiga += "'" + vals[v] + "',"
            # Tolgo l'ultima virgola
            queryRiga = queryRiga[:-1]
            queryRiga += ")"
            cursor.execute(queryRiga)

if((sys.argv.__len__()) != 3):
    print("Uso: nomeScript nomeFile/pathFile nomeDb")
else:
    creaDb("SourceSchema")
    creaDb("TargetSchema")