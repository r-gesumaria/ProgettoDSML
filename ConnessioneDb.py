import mysql.connector
import xml.etree.ElementTree as ET

tree = ET.parse('metadataBigBig.xml')
root = tree.getroot()
table = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database = "proviamoinsieme"
)
mycursor = mydb.cursor()
print(mydb.is_connected())

for c in root.findall("./Schemas/SourceSchema/Relation"):
    nameEn = c.get('name')
    table = 'CREATE TABLE '+ nameEn + ' ('

    attributi = root.findall("./Schemas/SourceSchema/*[@name='" + nameEn + "']/Attr")
    for a in attributi:
       table += a.find('Name').text
       if(a.find('DataType').text == 'TEXT'):
           table += ' varchar(100),'

    table = table [:-1]
    table += ')'
    mycursor.execute(table)

print(table)




