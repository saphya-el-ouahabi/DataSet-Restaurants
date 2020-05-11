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

#On ouvre le site de L'Internaute sur les restaurants de la Haute-Savoie
html = urlopen("https://www.linternaute.com/restaurant/guide/dept-haute-savoie/")
html_soup = BeautifulSoup(html, 'html.parser')
# On recupère tous les titres (les noms des restaurants et le lien) 

listeLienResto=[]
rows = html_soup.findAll("h2")
nbResto=len(rows)
cpt=0
data=[]
listeResto=[]
#on parcourt l'ensemble des restos de la page
for i in rows:
    for j in i:
        listeDonnees=[]
        
        # Nom du restaurant
        for nom in j:
            listeDonnees.append(nom)
            
        # Lien du restaurant
        lienResto="https://www.linternaute.com/"+j.get("href")
        listeDonnees.append(lienResto)
        
        #On ouvre la page d'un resto
        html_resto = urlopen(lienResto)
        html_resto_soup = BeautifulSoup(html_resto, 'html.parser')
        
        # Numero de telephone du Restaurant
        listeDonnees.append(html_resto_soup.findAll("li",{"class":"icomoon-phone"})[0].a.get("href"))
        
        # Localisation du Restaurant
        rue_rows=html_resto_soup.findAll("li",{"class":"icomoon-location"})
        html_adresse=html_resto_soup.findAll("li",{"class":"icomoon-location"})[0]
        for i in range(0,len(html_adresse.findAll("span"))):
            #Si un des champs (rue, code postal ou ville) n'est pas rensigne on ajoute
            #une chaine de caractere vide
            if len(html_adresse.findAll("span")[i]) == 0:
                    listeDonnees.append("")
            for j in (html_adresse.findAll("span")[i]):
                    #strip() permet d'ignorer les \n et \r
                    listeDonnees.append(j.strip())       
            
        # Budget du restaurant
        budget_rows=html_soup.findAll("div",{"class":"grid_col w75 bu_restaurant_details"})[cpt].ul.findAll("a")
        for budget in budget_rows:
            if "budget" in budget.get("href"):
                cpt=cpt+1
                listeDonnees.append(budget.text.strip())
                
        # Note du restaurant
        note_rows = html_resto_soup.findAll("span",{"class":"bu_restaurant_grade"})
        for i in note_rows[0].span:
            listeDonnees.append(" "+i+" / 5 ☆")   
        
        #Avis les plus pertinents
        #On cree une liste d'avis initialisee a vide
        liste_avis=[]
        avis_rows = html_resto_soup.findAll("p",{"itemprop":"description"})
        for a in avis_rows :
            #On ajoute les differents avis dans la liste
            liste_avis.append(a.text.strip())
        #On concatene cette liste en une chaine de caractere
        avis =''.join(str(elem) for elem in liste_avis)
        #On ignore les \n, \r, \t et ; presents dans les avis
        regex = re.compile(r'[\n\r\t;]')
        avis = regex.sub(" ", avis)
        #On ajoute les avis dans la listeDonnees
        listeDonnees.append(avis)
        
        #Site internet
        #On regarde si le resto possede un lien vers son site internet
        if len(html_resto_soup.findAll("a",{"class":"bu_restaurant_btn_square"})) != 0:
            #Si oui on l'ajoute dans notre listeDonnees
            listeDonnees.append(html_resto_soup.findAll("a",{"class":"bu_restaurant_btn_square"})[0].get("href"))
        else:
            #Sinon on indique non connu
            listeDonnees.append("NC")
        
    
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
   
for i in range(2,int(dernierNum)+1):
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
            
            # Numero de telephone du Restaurant
            if len(html_resto_soup.findAll("li",{"class":"icomoon-phone"})) != 0:
                listeDonnees.append(html_resto_soup.findAll("li",{"class":"icomoon-phone"})[0].a.get("href"))
            else:
                listeDonnees.append("")
                
            # Localisation du Restaurant
            rue_rows=html_resto_soup.findAll("li",{"class":"icomoon-location"})
            html_adresse=rue_rows[0]
            for i in range(0,len(html_adresse.findAll("span"))):
                #Si un des champs (rue, code postal ou ville) n'est pas rensigne on ajoute
                #une chaine de caractere vide
                if len(html_adresse.findAll("span")[i]) == 0:
                    listeDonnees.append("")
                #sinon on ajoute l'adresse a la listeDonnees
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
            for i in note_rows[0].span:
                listeDonnees.append(" "+i+" / 5 ☆") 
            
            #Avis les plus pertinents
            #On cree une liste d'avis initialisee a vide
            liste_avis=[]
            avis_rows = html_resto_soup.findAll("p",{"itemprop":"description"})
            for a in avis_rows :
                #On ajoute les differents avis dans la liste
                liste_avis.append(a.text.strip())
            #On concatene cette liste en une chaine de caractere
            avis =''.join(str(elem) for elem in liste_avis)
            #On ignore les \n, \r, \t et ; presents dans les avis
            regex = re.compile(r'[\n\r\t;]')
            avis = regex.sub(" ", avis)
            #On ajoute les avis dans la listeDonnees
            listeDonnees.append(avis)
            
            #Site internet
            #On regarde si le resto possede un lien vers son site internet
            if len(html_resto_soup.findAll("a",{"class":"bu_restaurant_btn_square"})) != 0:
                #Si oui on l'ajoute dans notre listeDonnees
                listeDonnees.append(html_resto_soup.findAll("a",{"class":"bu_restaurant_btn_square"})[0].get("href"))
            else:
                #Sinon on indique non connu
                listeDonnees.append("NC")
            
            #On ajoute a notre liste data la listeDonnees 
            data.append(listeDonnees)

print("Il y a "+str(nbResto)+" restaurants")




"""========================================================================="""
# Fichier CSV
"""========================================================================="""

#On cree les differentes entetes de notre fichier csv
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
     u'Site internet'
]


   
print(data)

#On cree un fichier csv dans lequel on va ajouter nos donnees
with open('databaseResto.csv', 'w',encoding="utf-8") as f:
    #On ajoute les entetes crees precedement
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    i=0
    #On parcourt notre liste de data
    for i in data:
        #Dans chaque ligne de notre fichier on ajoute nos donnees
        ligne = ";".join(i) + "\n"
        f.write(ligne)

    f.close()

#On ouvre le fichier csv
dataRestos = pd.read_csv("databaseResto.csv", sep=';', encoding="utf-8")

#On recupere la colonne des notes
notes=dataRestos['Note']
#On stocke la note minimale attribuee
min_note=min(notes)
#On stocke la note maximale attribuee
max_note=max(notes)
#On recupere la colonne des noms
noms=dataRestos['Nom']

#On cree une liste, initialisee à vide, qui contiendra les restaurants ayant la note min
resto_min=[]
#On cree une liste, initialisee à vide, qui contiendra les restaurants ayant la note max
resto_max=[]
#On parcourt les notes
for i,n in enumerate(notes):
    #Quand une note est la note min
    if n==min_note:
        #On ajoute a la liste resto_min le nom du resto associe a cette note
        resto_min.append(noms[i])
    #Quand une note est la note max
    if n==max_note:
        #On ajoute a la liste resto_max le nom du resto associe a cette note
        resto_max.append(noms[i])


print('Les resto les moins bien notes',resto_min)
print('les restos les mieux notes',resto_max)
