# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:59:44 2020

@author: Sophya
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

html = urlopen("https://www.linternaute.com/restaurant/guide/dept-haute-savoie/")
html_soup = BeautifulSoup(html, 'html.parser')

rows = html_soup.findAll("h2")
pages= html_soup.findAll("a",{"class":"JpaginatorLink"},"href")
print(len(pages))

liste_lien=[]
for page in pages:
    #print(page)
    link= page.get("href")
    liste_lien.append(link)

leLien=liste_lien[len(liste_lien)-2]
resteLien=""
dernierNum=""
passe=False
for i in leLien:
    if not passe :
        resteLien=resteLien+i
        print("i=",i)
        if i== "=":
            passe=True
    else :
        dernierNum=dernierNum+i

print("coucou"+resteLien)
print("Derniere page : "+dernierNum)

 
print("c'est lui"+liste_lien[len(liste_lien)-2])

print("nombre de restos",len(rows))

print("Nom des restos :")
listeResto=[]
for i in rows:
    for j in i:
        for a in j:
            listeResto.append(a)
print(listeResto)
#print(len(rows))



for i in range(2,int(dernierNum)+1,1):
    html = urlopen("https://www.linternaute.com/"+resteLien+str(i))
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("h2")
    listeR=[]

    print("Nom des restos :")
    c=[]
    for i in rows:
        for j in i:
            for a in j:
                listeR.append(a)
    print(listeR)
