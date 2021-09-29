from types import resolve_bases
import xml.etree.ElementTree as ET
import requests
from datetime import date, timedelta
import os

def request_Url(data = date.today()):
    ano = (data.year)
    mes = (f"{data.month:02d}")
    dia = (f"{data.day:02d}")
    arquivo = f'feed{ano}{mes}{dia}.xml'
    url = f"https://www.jornalminasgerais.mg.gov.br/modulos/casacivil.jornalminasgerais/diarioOficial/{ano}/{mes}/{dia}/jornal/caderno1_{ano}-{mes}-{dia}.xml"
    url_pdf = f"https://www.jornalminasgerais.mg.gov.br/modulos/casacivil.jornalminasgerais/diarioOficial/{ano}/{mes}/{dia}/jornal/caderno1_{ano}-{mes}-{dia}.pdf"
    #print(url)
    r = requests.get(url)
    with open(arquivo, 'wb') as file:
        file.write(r.content)
    #return (r.text)
    result = {'arquivo':arquivo, 'url_pdf': url_pdf}
    #print(result)
    return result
    
def find_in_tree(tree, node):
    found = tree.find(node)
    if found == None:
        print ("No %s in file" % node)
        found = []
    return found  

today = date.today()
for i in range(0,1):
    novadata = (today - timedelta(days=i))
    try:
        #xmlfile = "feed20210902.xml"
        dict_caderno = request_Url(novadata)
        xmlfile = dict_caderno['arquivo']
        url_pdf = dict_caderno['url_pdf']
        
        #print(xmlfile)

        xmlp = ET.XMLParser(encoding="ISO-8859-1")
        root = ET.parse(xmlfile,parser=xmlp).getroot()

        datacaderno = (root.attrib['data'])

        fwdefs = find_in_tree(root,"caderno")
        fwdefs = find_in_tree(fwdefs,"blocos")
        fwdefs = find_in_tree(fwdefs,"indice")

        der_node = []


        for item in fwdefs:
            
            #print(item.attrib['nome'])
            if "Mobilidade" in item.attrib['nome']:
                #print(item.attrib)
                for elem in item.iter():
                    if ("Estradas" in elem.attrib['nome']):
                        der_node = elem

        if type(der_node) is list:
            print(f"{datacaderno} Não há publicações sobre o DER/MG.")
            print(f"    Link para download: {url_pdf}")
        else:
            nome = (der_node.attrib['nome'])
            inicio = (der_node.attrib['inicio'])
            fim = (der_node.attrib['fim'])
            if inicio == fim:
                print(f"{datacaderno} {nome}: página {inicio}.")
            else: 
                print(f"{datacaderno} {nome}: páginas {inicio} a {fim}.")
            print(f"    Link para download: {url_pdf}")

        
    except Exception as e:
        print(f"{novadata} Erro ao obter arquivo. Erro -> {e}.")
        
    os.remove(xmlfile) #Remove o XML baixado







