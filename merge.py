#ePO policy policy combiner / merger
#Author: w00f - github.com/w00fx
#0.1 version

from xml.etree import ElementTree
import re
import sys

def xml_id_parse(xml):
#Gerado para criar as lista de ID das políticas
#Function used for create lists of IDs of policies
    print('[+] Generate IDs of '+xml)
    with open(xml, 'rt') as f:
        tree = ElementTree.parse(f)
    results = []
    for node in tree.findall('.//Setting'):
        name = node.attrib.get('name')
        value = node.attrib.get('value')
        if name == 'RuleID' and '_' not in value:
            results.append(value)
    return results


#Usado para separar os elementos do arquivo em lista
#Function used to separate elements of xml in lists
def xml_parse(xml, arg):
    print('[+] Parsing '+ xml)
    file = open(xml, 'r')
    file = file.read()
    list = re.split(r''+arg, file)
    return list


#Usodo para inserir as políticas no xml
#Function used for insert policies on xml
def insert_policies(list1, list2, list3):
    print('[+] Inserting policies')
    for i in list2:
        j = 1
        while j < len(list3):
            if i in list3[j]:
                list1.insert(3,list3[j])
                break
            j = j + 1
    return list1
xml_with_policies = input("Name of xml with policies (with .xml on final): ")
xml_client = input("Name of xml with needs policies (with .xml on final): ")

ids_policies = []
xml1 = xml_id_parse(xml_with_policies)
xml2 = xml_id_parse(xml_client)

#Aqui vamos gerar uma lista daquilo que não tem na politica do cliente, com as IDs
#Here we gonna generate a list of what is don't on the policies of cliente, with the IDs
for i in xml1:
    if i not in xml2:
        ids_policies.append(i)

list1 = xml_parse(xml_with_policies, '</EPOPolicySettings>')
list2 = xml_parse(xml_client, '</EPOPolicySettings>')

#Pegando o resultado e juntando
#Taking the first result and joining
resultado1 = insert_policies(list2, ids_policies, list1)
resultado1 = '</EPOPolicySettings>'.join(resultado1)

#Parsing for insert <PolicySettings> in the last lines
list3 = resultado1.split('</PolicySettings>')
list4 = xml_parse(xml_with_policies, '</PolicySettings>')

#Again taking the results
resultado2 = insert_policies(list3, ids_policies, list4)
resultado2 = '</PolicySettings>'.join(resultado2)

#Final results being Processed
arq = input("Insert the file name with .xml on final: ")
resultado_final = open(arq, 'w')
resultado_final.write(resultado2)
resultado_final.close()
print('[+] Done with', arq, 'name. Just import in ePO for using')
