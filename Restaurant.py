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
import re
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
cpt=0
data=[]
listeResto=[]
for i in rows:
    for j in i:
        listeDonnees=[]
        
        # Nom du restaurant
        for nom in j:
            listeDonnees.append(nom)
            
        # Lien du restaurant
        lienResto="https://www.linternaute.com/"+j.get("href")
        listeDonnees.append(lienResto)
        
        html_resto = urlopen(lienResto)
        html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
        
        # Numero du Restaurant
        listeDonnees.append(html_resto_soup.findAll("li",{"class":"icomoon-phone"})[0].a.get("href"))
        
        # Localisation du Restaurant
        rue_rows=html_resto_soup.findAll("li",{"class":"icomoon-location"})
        html_adresse=html_resto_soup.findAll("li",{"class":"icomoon-location"})[0]
        for i in range(0,len(html_adresse.findAll("span"))):
            for j in (html_adresse.findAll("span")[i]):
                listeDonnees.append(j.strip())       
            
        # Budget du restaurant
        budget_rows=html_soup.findAll("div",{"class":"grid_col w75 bu_restaurant_details"})[cpt].ul.findAll("a")
        for budget in budget_rows:
            if "budget" in budget.get("href"):
                cpt=cpt+1
                listeDonnees.append(budget.text.strip())
                
        # Note du restaurant
        note_rows = html_resto_soup.findAll("span",{"class":"bu_restaurant_grade"})
        for i in html_resto_soup.findAll("span",{"class":"bu_restaurant_grade"})[0].span:
            listeDonnees.append(" "+i+" / 5 ☆")   
        
        #Avis les plus pertinents
        liste_avis=[]
        avis_rows = html_resto_soup.findAll("p",{"itemprop":"description"})
        for avis in avis_rows :
            liste_avis.append(avis.text.strip())
        a_vis =''.join(str(elem) for elem in liste_avis)
        regex = re.compile(r'[\n\r\t]')
        a_vis = regex.sub(" ", a_vis)
        listeDonnees.append(a_vis)
        
    
        data.append(listeDonnees)
print("premiere page finie")

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
   
for i in range(2,3):#int(dernierNum)+1,1):
    html = urlopen("https://www.linternaute.com"+resteLien+str(i))
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.findAll("h2")
    nbResto=nbResto+len(rows)
    po=5
    cpt=0
    for i in rows:
        po=po+1
        listeDonnees=[]
        for j in i:
            listeLienResto.append(j.get("href"))
            listeDonnees=[]
            
            # Nom du Restaurant
            for nom in j:
                listeDonnees.append(nom)
                
            # Lien du Restaurant
            lienResto="https://www.linternaute.com/"+j.get("href")
            listeDonnees.append(lienResto)
        
            html_resto = urlopen(lienResto)
            html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
            
            # Numero du Restaurant
            if len(html_resto_soup.findAll("li",{"class":"icomoon-phone"})) != 0:
                listeDonnees.append(html_resto_soup.findAll("li",{"class":"icomoon-phone"})[0].a.get("href"))
            else:
                listeDonnees.append("")
            # Localisation du Restaurant
            rue_rows=html_resto_soup.findAll("li",{"class":"icomoon-location"})
            html_adresse=html_resto_soup.findAll("li",{"class":"icomoon-location"})[0]
            for i in range(0,len(html_adresse.findAll("span"))):
                for j in (html_adresse.findAll("span")[i]):
                    listeDonnees.append(j.strip()) 
                
            # Budget du restaurant
            budget_rows=html_soup.findAll("div",{"class":"grid_col w75 bu_restaurant_details"})[cpt].ul.findAll("a")
            for budget in budget_rows:
                if "budget" in budget.get("href"):
                    cpt=cpt+1
                    listeDonnees.append(budget.text.strip())
                    
            # Note du restaurant
            note_rows = html_resto_soup.findAll("span",{"class":"bu_restaurant_grade"})
            for i in html_resto_soup.findAll("span",{"class":"bu_restaurant_grade"})[0].span:
                listeDonnees.append(" "+i+" / 5 ☆") 
            
            #Avis les plus pertinents
            liste_avis=[]
            avis_rows = html_resto_soup.findAll("p",{"itemprop":"description"})
            for avis in avis_rows :
                liste_avis.append(avis.text.strip())
            a_vis =''.join(str(elem) for elem in liste_avis)
            regex = re.compile(r'[\n\r\t]')
            a_vis = regex.sub(" ", a_vis)
            listeDonnees.append(a_vis)
            data.append(listeDonnees)

print("Il y a "+str(nbResto)+" restaurants")




"""========================================================================="""
# Fichier CSV
"""========================================================================="""

entetes = [
     u'Nom',
     u'Lien',
     u'Telephone',
     u'Rue',
     u'Code Postal',
     u'Ville',
     u'Budget',
     u'Note',
     u'Avis',
     u'Menu'
]


   
print(data)

with open('databaseResto.csv', 'w',encoding="utf-8") as f:
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    i=0
    for i in data:
        
        
        ligne = ";".join(i) + "\n"
        f.write(ligne)

    f.close()