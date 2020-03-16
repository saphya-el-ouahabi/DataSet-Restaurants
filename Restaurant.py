# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:32:44 2020

@author: elsar
"""
" IMPORTATION  "
"------------------------------------------------------------------------------"
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
"------------------------------------------------------------------------------"

# On regarde la page 1

html = urlopen("https://www.linternaute.com/restaurant/guide/dept-haute-savoie/")
html_soup = BeautifulSoup(html, 'html.parser')
# On recupère tous les titres (les noms des restaurants et le lien) 

# On s'occupe d'abord des noms des restaurants

rows = html_soup.findAll("h2")
nbResto=len(rows)

print("Nom des restos :")
listeResto=[]
for i in rows:
    for j in i:
        link= j.get("href")
        print(link)
        for a in j:
            listeResto.append(a)
print(listeResto)
print("")

# Ensuite on recupere le lien des restaurants

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
    
    
# On refait la meme chose pour toutes les pages 
   
for i in range(2,int(dernierNum)+1,1):
    html = urlopen("https://www.linternaute.com"+resteLien+str(i))
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("h2")
    listeR=[]
    
    #print("\n Nom des restos : \n")
    c=[]
    nbResto=nbResto+len(rows)
    for i in rows:
        for j in i:
            link= j.get("href")
            print(link)
            for a in j:
                listeR.append(a)
    #print(listeR)


#lienResto=html_soup.findAll("a",{"class":"bu_restaurant_title_2"},"href")
#listeLienResto=[]
#print("jshfjhfkjdshkj",lienResto)
for lien in lienResto:
    print(lien)
    #link= lien.get("href")
    #print("a = ",link)
    #listeLienResto.append(link)

#print('liste = ',listeLienResto)

print("Il y a "+str(nbResto)+" restaurants")