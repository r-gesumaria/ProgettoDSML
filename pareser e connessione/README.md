Di seguiro sarà mostrato come eseguire gli script python.

Per eseguire lo script ConnessioneDb.py bisogna utilizzare il seguente comando:
```
python3 ConnessioneDb.py pathFile.xml nomeDb
```
Dove:
-	ConnessioneDb.py, è il nome dello script che si vuole eseguire;
-	pathFile.xml, è il nome del file dal quale si vuole acquisire la struttura del database;
-	nomeDb, è il suffisso del nome che verrà dato ai database che saranno creati per il source e il target schema. 

Per eseguire lo script Parser.py bisogna utilizzare il seguente comando:
```
python3 Parser.py pathFile.xml nomeFile
```
Dove:
-	Parser.py, è il nome dello script che si vuole eseguire;
-	pathFile.xml, è il nome del file xml che si vuole convertire;
-	nomeFile, è il suffisso del nome che verrà dato ai file finali xmi per il source e il target schema.

Cosa importante da ricordare è che, per non avere problemi con l’utilizzo dei file con il tool CoDIT, in nomeFile non utilizzare il segno di punteggiatura “punto”.
