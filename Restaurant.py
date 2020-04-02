# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:32:44 2020

@author: elsar
"""
" IMPORTATION  "
#------------------------------------------------------------------------------
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
#------------------------------------------------------------------------------

"""========================================================================="""
# On regarde la page 1
"""========================================================================="""

html = urlopen("https://www.linternaute.com/restaurant/guide/dept-haute-savoie/")
html_soup = BeautifulSoup(html, 'html.parser')
# On recupère tous les titres (les noms des restaurants et le lien) 

listeLienResto=[]
rows = html_soup.findAll("h2")
nbResto=len(rows)

data=[]
print("Nom des restos :")
listeResto=[]
for i in rows:
    for j in i:
        listeDonnees=[]
        #print("coucou")
        for nom in j:
            listeDonnees.append(nom)
        listeDonnees.append(j.get("href"))
        html_resto = urlopen("https://www.linternaute.com/"+j.get("href"))
        html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
        rue_rows=html_resto_soup.findAll("span",{"itemprop":"streetAddress"})
        postal_rows=html_resto_soup.findAll("span",{"itemprop":"postalCode"})
        ville_rows=html_resto_soup.findAll("span",{"itemprop":"addressLocality"})
        for i in rue_rows :
            for j in i:
                rue=j
                listeDonnees.append(j)
        for i in ville_rows:
            for j in i:
                ville=j
                listeDonnees.append(j)
        for i in postal_rows:
            for j in i:
                code=j
                listeDonnees.append(j)
    
        data.append(listeDonnees)
print("")

"""========================================================================="""
# Ensuite on recupere le lien des autres pages ainsi que le numero
# de la derniere page
"""========================================================================="""

pages= html_soup.findAll("a",{"class":"JpaginatorLink"},"href")
liste_lien=[]

for page in pages:
    link= page.get("href")
    liste_lien.append(link)
    
leLien=liste_lien[len(liste_lien)-2]
resteLien=""
dernierNum=""
passe=False
for i in leLien:
    if not passe :
        resteLien=resteLien+i
        if i== "=":
            passe=True
    else :
        dernierNum=dernierNum+i

print("Derniere page : "+dernierNum)
    
"""========================================================================="""
# On refait la premiere etape pour toutes les pages 
"""========================================================================="""
   
for i in range(2,int(dernierNum)+1,1):
    html = urlopen("https://www.linternaute.com"+resteLien+str(i))
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("h2")
    nbResto=nbResto+len(rows)
    po=5
    for i in rows:
        po=po+1
        #print(i)
        #print("oh")
        listeDonnees=[]
        for j in i:
            listeLienResto.append(j.get("href"))
            listeDonnees=[]
            for nom in j:
                listeDonnees.append(nom)
            listeDonnees.append(j.get("href"))
            html_resto = urlopen("https://www.linternaute.com/"+j.get("href"))
            html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
            rue_rows=html_resto_soup.findAll("span",{"itemprop":"streetAddress"})
            postal_rows=html_resto_soup.findAll("span",{"itemprop":"postalCode"})
            ville_rows=html_resto_soup.findAll("span",{"itemprop":"addressLocality"})
            for i in rue_rows :
                for j in i:
                    rue=j
                    listeDonnees.append(j)
            for i in ville_rows:
                for j in i:
                    ville=j
                    listeDonnees.append(j)
            for i in postal_rows:
                for j in i:
                    code=j
                    listeDonnees.append(j)
            data.append(listeDonnees)
#print(listeResto)

#print('liste = ',listeLienResto)

# print("Il y a "+str(nbResto)+" restaurants")

# html_resto = urlopen("https://www.linternaute.com/restaurant/restaurant/166592/chez-baud.shtml")
# html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
# rows=html_resto_soup.findAll("span",{"itemprop":"streetAddress"})

# adresse=""
# for i in rows :
#     #print(i)
#     for j in i:
#         print(j)


"""========================================================================="""
# Fichier CSV
"""========================================================================="""

entetes = [
     u'Nom',
     u'Lien',
     u'Telephone',
     u'Numero de rue',
     u'rue',
     u'Ville',
     u'Code Postal',
     u'Menu'
]

'''On veut supprimer les \n qui se trouve dans les differentes listes de donnees'''
#on parcourt les listes contenues dans data
for d in data:
    #on parcourt chaque element de chaque liste et strip() permet d'enlever les \n
    for i in range(0,len(d),1):
        d[i]=d[i].strip()
print(data)

with open('databaseResto.csv', 'w',encoding="utf-8") as f:
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    i=0
    for i in data:
        ligne = ";".join(i) + "\n"
        f.write(ligne)

    f.close()
