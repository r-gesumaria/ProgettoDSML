import xml.etree.ElementTree as ET
import sys
import re

def creaSchema(tipoSchema):
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # struttura della prima sezione del nuovo file
    newRoot = ET.Element('uml:Model')
    newRoot.attrib['xmi:version'] = '2.1'
    newRoot.attrib['xmlns:xmi'] = 'http://schema.omg.org/spec/XMI/2.1'
    newRoot.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    newRoot.attrib['xmlns:uml'] = 'http://schema.omg.org/spec/UML/2.1.1'
    newRoot.attrib['xsi:schemaLocation'] = 'http://schema.omg.org/spec/UML/2.1.1 http://www.eclipse.org/uml2/2.0.0/UML'
    newRoot.attrib['xmi:id'] = '_XrSbENk5EdyEZoPpUv3LUw'
    newRoot.attrib['name'] = 'Blank Model'
    packageImport = ET.SubElement(newRoot, 'packageImport')
    packageImport.attrib['xmi:type'] = 'uml:PackageImport'
    packageImport.attrib['xmi:id'] = '_XrSbEdk5EdyEZoPpUv3LUw'
    importedPackage = ET.SubElement(packageImport, 'importedPackage')
    importedPackage.attrib['xmi:type'] = 'uml:Model'
    importedPackage.attrib['href'] = 'http://schema.omg.org/spec/UML/2.1.1/uml.xml#_0'

    # ottengo tutte le entità dall'xml e creo gli elementi per il nuovo file
    for c in root.findall("./Schemas/" + tipoSchema + "/Relation"):

        nameEn = c.get('name')
        en = ET.SubElement(newRoot, "packagedElement")  # elemento per la definizione delle entita
        en.attrib['xmi:id'] = nameEn
        en.attrib['name'] = nameEn
        en.attrib['xmi:type'] = 'uml:Class'
        en.attrib['visibility'] = 'private'

        # estezione per la definizione di una entità
        ext = ET.SubElement(en, 'xmi:Extension')
        ann = ET.SubElement(ext, 'eAnnotations')
        ann.attrib['xmi:id'] = 'activityEAnnotation'  # controllare che vada bene che si mantenga sempre questo id
        ann.attrib['source'] = 'http://www.eclipse.org/uml2/2.0.0/UML'
        det = ET.SubElement(ann, 'details')
        det.attrib['xmi:id'] = 'phpbb_f_Entity'
        det.attrib['key'] = 'Entity'

        # ottengo il nome della PK
        namePk = root.find("./Schemas/"+tipoSchema+"/*[@name='" + nameEn + "']/PrimaryKey/Attr").text

        # per ogni entità crea gli attibuti relativi
        for a in root.findall("./Schemas/"+tipoSchema+"/*[@name='" + nameEn + "']/Attr"):

            attr = ET.SubElement(en, "ownedAttribute")

            # creo la sezione per identificare la PK
            if (a.find('Name').text == namePk):
                extPK = ET.SubElement(attr, 'xmi:Extension')
                annPK = ET.SubElement(extPK, 'eAnnotations')
                annPK.attrib['xmi:id'] = '_Ovi-VuPdEdy8F_b8rGg0Zw'
                annPK.attrib['source'] = 'http://www.eclipse.org/uml2/2.0.0/UML'
                detPK = ET.SubElement(annPK, 'details')
                detPK.attrib['xmi:id'] = '_Ovi-V-PdEdy8F_b8rGg0Zw'
                detPK.attrib['key'] = 'PK'

            attr.attrib['xmi:type'] = 'uml:Property'
            attr.attrib['xmi:id'] = a.find('Name').text
            attr.attrib['name'] = a.find('Name').text
            attr.attrib['visibility'] = 'private'

    # generiamo la sezione per le relazioni tra le entità
    list = root.findall("./Schemas/"+tipoSchema+"/ForeignKey")
    for fk in list:
        nomeEnt1 = fk.find("From").get("tableref")
        nomeEnt2 = fk.find("To").get("tableref")

        if (nomeEnt1 != '' and nomeEnt2 != ''):
            rel = ET.SubElement(newRoot, 'packagedElement')
            rel.attrib['xmi:type'] = 'uml:Association'
            rel.attrib['xmi:id'] = nomeEnt1 + "__" + nomeEnt2 + "__id"

    # struttura della sezione finale del nuovo file
    profileApplication = ET.SubElement(newRoot, 'profileApplication')
    profileApplication.attrib['xmi:type'] = 'uml:ProfileApplication'
    profileApplication.attrib['xmi:id'] = '_XrSbHdk5EdyEZoPpUv3LUw'
    extension2 = ET.SubElement(profileApplication, 'xmi:Extension')
    ann2 = ET.SubElement(extension2, 'eAnnotations')
    ann2.attrib['xmi:type'] = 'ecore:EAnnotation'
    ann2.attrib['xmi:id'] = '_XrSbHtk5EdyEZoPpUv3LUw'
    ann2.attrib['source'] = 'http://www.eclipse.org/uml2/2.0.0/UML'
    references = ET.SubElement(ann2, 'references')
    references.attrib['xmi:type'] = 'ecore:EPackage'  # da provare a togliere
    references.attrib['href'] = 'http://schema.omg.org/spec/UML/2.1.1/StandardProfileL2.xmi#_yzU58YinEdqtvbnfB2L_5w'
    appliedProfile = ET.SubElement(profileApplication, 'appliedProfile')
    appliedProfile.attrib['xmi:type'] = 'uml:Profile'
    appliedProfile.attrib['href'] = 'http://schema.omg.org/spec/UML/2.1.1/StandardProfileL2.xmi#_0'

    # scrivo l'albero creato sul nuovo file
    newTree = ET.ElementTree(newRoot)
    newTree.write(tipoSchema+"_"+sys.argv[2] + '.xmi')

if ((sys.argv.__len__()) != 3):
    print("Uso: nomeScript nomeFile/pathFile nomeFileXmi")
else:
    creaSchema("SourceSchema")
    creaSchema("TargetSchema")


