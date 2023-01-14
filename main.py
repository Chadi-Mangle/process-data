import csv #Bibliothèque permetant de manipuler les fichiers csv en Python

############### FONCTION UTILITAIRE ###############


def fixed()->None: 
    """
    Règle certains problèmes liées a la bibliothèque csv.
    """
    from os import listdir
    csvlist = listdir("./")
    for elem in csvlist: 
        if elem[len(elem)-4:] == ".csv": 
            f = open(elem, "r")
            text = f.read().replace("\n\n", "\n")
            f = open(elem, "w")
            f.write(text)
            f.close()

#"str:str"  le :str permet de dire que la variable str est une chaine de caractère. 
# "->float" permet d'exprimer le faites que l'objet retourner est un nombre flotant
def str_to_float(str:str)->float:  
    """
    Convertie une chaine de caractère en nombre flotant.
    str correspond a chaine de caractère que l'on convertir. 
    """
    try: 
        # Remplace si il ya besion les virgule par des points. 
        # Ce qui permet de pas avoir de problème lors de la conversion en entier ou floant de n'importe quel base de donnée
        return float(str.replace(",", '.')) 
    except: #l'erreur que l'on peut avoir c'est d'avoir un nombre entier a la place d'une chaine de caractère. 
        #Or comme replace() ne marche pas pour les nombre entiers cela crée une erreur
        #Jj'ai décidé avec cette fonction de convertir quand même les entiers en flotant
        return float(str)


############### FONCTION DE CALCUL ###############


# "lst_d:list" permet de savoir que lst_d esr une list. 
# "key1:str, key2:str" et que key1 et key2 sont des chaines de caractères.
# ->list permet d'exprimer le faites que l'objet retourner est une liste
def addition(lst_d:list, key1:str, key2:str)->list: 
    """
    Crée une liste de dictionnaire de l'addition entre deux valeurs des dictionnaires.  
    lst_d est une liste de dictionnaire.
    key1 et key2 sont des clé des dictionnaires de la listes.
    """
    list_donnees = []
    for elem in lst_d:
        dico = {key1+" et "+key2: str(int(str_to_float(elem[key1]) + str_to_float(elem[key2])))} # Créé un dictionaire de l'addition entre la valeur attribué à key1 et à key2
        list_donnees.append(dico)

    return list_donnees

def medium(lst_d:list)->list: 
    """
    Crée une liste de dictionnaire de la moyenne entre toutes les valeurs d'un dictionnaires.
    lst_d est une liste de dictionnaire.
    """
    list_donnees = []
    for elem in lst_d: 
        #converti la liste des nombres en nombres floatant en utilisant la fonction "str_to_float" definie plus haut
        elem_float = [str_to_float(i) for i in list(elem.values())] 
        dico = {"Moyenne": str(int(sum(list(elem_float))/len(list(elem_float))))} #ce qui permet de faire les calculs 
        list_donnees.append(dico)
    
    return list_donnees

def percentage(lst_d:list, key1:str, key2:str)->list:
    """
    Crée une liste de dictionnaire du pourcentage entre deux valeurs des dictionnaires.
    lst_d est une liste de dictionnaire.
    La valeur assosié à key1 doit être une moyenne.
    key2 sont des clé des dictionnaires de la liste. 
    """
    list_donnees = []
    for elem in lst_d:
        dico = {"Pourcentage de "+key1+" sur "+key2: str(int((str_to_float(elem[key1]) / str_to_float(elem[key2]))*100))+"%"}
        list_donnees.append(dico)

    return list_donnees

def rate_of_grow(lst_d:list, key1:str, key2:str)->list: #calcul le taux de croissance
    """
    Crée une liste de dictionnaire du calcul du taux de croissances entre deux valeurs des dictionnaires.
    lst_d est une liste de dictionnaire.
    key1 et key2 sont des clé des dictionnaires de la listes.
    """
    list_donnees = []
    for elem in lst_d:   
        try:  #  test si le deuxième element de la liste est égale à 0 car on ne peut pas faire de division par zéro
            grow = int((str_to_float(elem[key1]) - str_to_float(elem[key2])))/str_to_float(elem[key2])
        except: 
            grow = 0 
        dico = {"Taux de croissance entre "+key1 +" et "+ key2: str(grow)}
        list_donnees.append(dico)

    return list_donnees

def prediction_growing(lst_d:list, key1:str, key2:str)->list: 
    """ 
    Cree une liste de prediction a partir du taux de croissances (possitioné en key1).
    lst_d est une liste de dictionnaire.
    """
    list_donnees = []
    for elem in lst_d:
        #Le taux de croissance etant un pourcentages il faut ajouté 1 avant de faire la mutiplication
        grow = 1 + str_to_float(elem[key1]) 
        dico = {"Prediction avec "+key1 : str(int(grow* str_to_float(elem[key2])))} 
        list_donnees.append(dico)

    return list_donnees


############### FONCTION SUR LES LISTE, DICTIONNAIRE, CSV ET HTML ###############


def change_value_list_dictionary(d_to_change, second_d, key1, key2)->None: 
    """
    Change la valeur associé a "key1" de d_to_change en la cle "key2" du second_d.
    d_to_change et second_d sont des listes de dictionnaires.
    """
     #zip() permet d'avoir une itération parallèle des deux liste de dictionnaire.
     #Les elemment de d_to_change sont stocké dans elem_to_change et ceux de second_d dans elem
    for elem_to_change, elem in zip(d_to_change, second_d):
        elem_to_change[key1] = elem[key2]

def add_value_list_dictionary(d_to_change, second_d, key)->None: 
    """
    Ajoute la valeur associé a "key" de second_d au dictionnaires de d_to_change.
    d_to_change et second_d sont des listes de dictionnaires.
    """
    for elem_to_add, elem in zip(d_to_change, second_d):
        elem_to_add[key] = elem[key]

def change_logement_value(d): #Fonction utile pour ne pas avoir a recopier plusieurs fois les mêmes lignes de code. 
    """
    Addition les valeurs d'addition et établisment et logements 
    Remplace la valeur de logement par cette addition
    """
    # Liste de dictionaire de l'addition des établisments et logements 
    logements_etablissement = csv2dict("nb_abonees-fibre_departement_trimestre", ['Logements', 'Ã‰tablissements']) 
    d_logements_etablissement = addition(logements_etablissement, "Logements", "Ã‰tablissements")

    #changement des valeurs dans le dictionaire
    change_value_list_dictionary(d, d_logements_etablissement, "Logements", "Logements et Ã‰tablissements")

def csv2dict(filename, header)->list:
    """
    Transforme un csv en dictionaire.  
    filename est une chaine de caractère du nom de fichier csv. 
    header est une liste contenant les valeurs qui seront les utilisé comme clé de dictionnaire sortie.
    """
    from os.path  import exists
    #permet savoir le csv existe bien réelement
    assert exists(filename) != True, f'Le fichier "{filename}"" n\'a pas été trouvé.\nVous pouvez retélécharger les fichiers sources sur ce site : https://chadi-mangle.github.io/process-data/'
    list_donnees_csv = []
    f = open(filename+".csv", "r")
    csvreader = csv.DictReader(f, delimiter=";")
    for row in csvreader:
        dico = {}
        for elem in header: 
            dico[elem] = row[elem]
        list_donnees_csv.append(dico)
    return list_donnees_csv

def dict2csv(d:list, filename:str)->None:
    """
    Transforme la liste de dictionaire "d" en un fichier csv.
    """
    csvfile = open(filename+".csv" , "w")
    fieldnames = d[0].keys() #prend les clé du dictionnaires et temps que header
    writer = csv.DictWriter(csvfile ,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(d)
    csvfile.close()
    fixed()

def csv2html(filename:str, h1_and_tbody:str)->None: 
    """
    Crée un fichier html appartir d'un fichier csv. 
    h1_and_tbody est une varriable contenant le titre du site et le header du tableau htmls
    """
    f = open(filename+".html", "w")
    htmlfile = '<!DOCTYPE html><html lang="fr-FR"><head><meta charset="utf-8"><title>SAE 15</title><link rel="stylesheet" href="style.css"></head><body>'+ h1_and_tbody 
    csvfile = open(filename+".csv", "r")
    csvreader = csv.reader(csvfile)

    for row in csvreader: #permet d'avoir le first_value = header (première ligne du csv)
        first_value = row[0]
        break

    for row in csvreader: #
        if row[0] == first_value: #premet de ne pas avoir ces valeurs ecrit dans les tableaux
            pass
        else:
            htmlfile += "<tr>" 
            for elem in row: 
                htmlfile += "<th>{}</th>".format(elem)
            htmlfile += "</tr>" 

    htmlfile += "</tbody></table></div></body></html>"
    f.write(htmlfile) 


############### CREATION DES CSV ET HTML ###############


def nb_hab_avec_fibre_departements_annees():
    """
    Cree le csv nb_hab_avec_fibre_departements_annees
    """
    #Creéation d'une liste de dictionaire a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements', 'T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    change_logement_value(d)

    #création du nouveau csv et html
    dict2csv(d, "nb_abonees-fibre_departement_annees")
    csv2html("nb_abonees-fibre_departement_annees", '<h1>Nombre d\'habitation possÃ©dant la fibre par dÃ©partements et par annÃ©es.</h1><div><table><thead><tr><th>Code du dÃ©partements</th><th>Nom du dÃ©partements</th><th>Nombre d\'habitation</th><th>Logement avec la fibre en 2017</th><th>Logement avec la fibre en 2018</th><th>Logement avec la fibre en 2019</th><th>Logement avec la fibre en 2020</th><th>Logement avec la fibre en 2021</th><th>Logement avec la fibre en 2022</th></thead><tbody>')

def moy_fibre_departement_annees(): 
    """
    Cree le csv moy_fibre_departement_annees.
    """
    #Creéation d'une liste de dictionaire a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    # Creation du dictionaires pour le calcul de la moyenne
    annees_header = ['T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    med_annees= csv2dict("nb_abonees-fibre_departement_trimestre", annees_header)

    #calcul de la moyenne
    d_full_med = medium(med_annees)

    add_value_list_dictionary(d, d_full_med,"Moyenne")
    change_logement_value(d)

    #création du nouveau csv et html
    dict2csv(d, "moy_fibre_departement_annees")
    csv2html("moy_fibre_departement_annees", "<h1>Moyenne d'abonnÃ©s a la fibre par dÃ©partement.</h1><div><table><thead><tr><th>Code du dÃ©partements</th><th>Nom du dÃ©partements</th><th>Nombre d\'habitation</th><th>Moyenne d'abonnÃ©es sur 6 ans</th></thead><tbody>")

def percentage_fibre_departement_annees(): 
    """
    Cree le csv percentage_fibre_departement_annees.
    """
    #Creéation d'une liste de dictionaire a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    # Cre&tion du dictionaires pour le calcul de la moyenne
    annees_header = ['T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    med_annees= csv2dict("nb_abonees-fibre_departement_trimestre", annees_header)

    #calcul de la moyenne
    d_full_med = medium(med_annees)

    add_value_list_dictionary(d, d_full_med,"Moyenne")
    change_logement_value(d)

    # calcul du pourcentage 
    d_percentage = percentage(d,"Moyenne", 'Logements')
    change_value_list_dictionary(d, d_percentage,"Moyenne","Pourcentage de Moyenne sur Logements")

    #création du nouveau csv et html
    dict2csv(d, "percentage_fibre_departement_annees")
    csv2html("percentage_fibre_departement_annees", "<h1>Pourcentage d'abonnÃ©s a la fibre en moyenne par dÃ©partement.</h1><div><table><thead><tr><th>Code du dÃ©partements</th><th>Nom du dÃ©partements</th><th>Nombre d\'habitation</th><th>Pourcentage d'abonnÃ©es sur 6 ans: </th></thead><tbody>")

def prediction_fibre_departement(): 
    """
    Cree le csv prediction_fibre_departement.
    """
    #Creéation d'une liste de dictionaire a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements', 'T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)
    change_logement_value(d)

    #Calcul le taux de croissance entre 2021 et 2022
    d_grow = rate_of_grow(d,'T3 2022', 'T3 2021')
    add_value_list_dictionary(d, d_grow, 'Taux de croissance entre T3 2022 et T3 2021')
    
    #Fait les prediction pour 2023 en mutipliant le taux de croissances avec les valeurs de 2022
    d_2023_prediction = prediction_growing(d, 'Taux de croissance entre T3 2022 et T3 2021', 'T3 2022')
    change_value_list_dictionary(d, d_2023_prediction,'Taux de croissance entre T3 2022 et T3 2021', 'Prediction avec Taux de croissance entre T3 2022 et T3 2021')

    #création du nouveau csv et html
    dict2csv(d, "prediction_nb_abonees-fibre_departement_annees")
    csv2html("prediction_nb_abonees-fibre_departement_annees", '<h1>Nombre d\'habitation possÃ©dant la fibre par dÃ©partements et par annÃ©es avec prÃ©diction.</h1>  <div>    <table><thead><tr><th>Code du dÃ©partements</th><th>Nom du dÃ©partements</th><th>Nombre d\'habitation</th><th>Logement avec la fibre en 2017</th><th>Logement avec la fibre en 2018</th><th>Logement avec la fibre en 2019</th><th>Logement avec la fibre en 2020</th><th>Logement avec la fibre en 2021</th><th>Logement avec la fibre en 2022</th><th>PrÃ©diction pour 2023</th></thead><tbody>')


#Permet d'exécuter du code lorsque le fichier s'exécute en tant que script, mais pas lorsqu'il est importé en tant que module
if __name__ == "__main__": 
    nb_hab_avec_fibre_departements_annees()
    moy_fibre_departement_annees()
    percentage_fibre_departement_annees()
    prediction_fibre_departement()
    print("Tous les fichiers ont bien été généré")