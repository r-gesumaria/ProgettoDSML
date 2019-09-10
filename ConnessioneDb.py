import xml.etree.ElementTree as ET
import mysql.connector
import sys

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
    nomeDb = tipoSchema + sys.argv[2]
    mycursor.execute("CREATE DATABASE " + nomeDb)
    mydb.close

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    table = ""

    #connessione al db appena creato e generazione delle tabelle con attributi
    mydb = creaConnessione(nomeDb)

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

    print(table)

if((sys.argv.__len__()) != 3):
    print("Uso: nomeScript nomeFile/pathFile nomeDb")
else:
    creaDb("SourceSchema")
    creaDb("TargetSchema")


