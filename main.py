import csv #Bibliothèque permettant de manipuler les fichiers csv en Python

############### FONCTION UTILITAIRE ###############


def fixed()->None: 
    """
    Règle certains problèmes liés à  la bibliothèque csv.
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

#"str:str"  le :str permet de dire que la variable str est une chaine de caractères. 
# "->float" permet d'exprimer le fait que l'objet retourné est un nombre flottant
def str_to_float(str:str)->float:  
    """
    Convertit une chaine de caractères en nombre flottant.
    str correspond à chaine de caractères que l'on convertit. 
    """
    try: 
        # Remplace s'il y a besoin les virgules par des points. 
        # Ce qui permet de ne pas avoir de problème lors de la conversion en entier ou flottant de n'importe quel base de données
        return float(str.replace(",", '.')) 
    except: #l'erreur que l'on peut avoir c'est d'avoir un nombre entier à la place d'une chaine de caractères. 
        #Or comme replace() ne marche pas pour les nombres entiers cela créé une erreur
        #J'ai décidé avec cette fonction de convertir quand même les entiers en flottant
        return float(str)


############### FONCTION DE CALCUL ###############


# "lst_d:list" permet de savoir que lst_d est une liste. 
# "key1:str, key2:str" et que key1 et key2 sont des chaines de caractères.
# ->list permet d'exprimer le fait que l'objet retourné est une liste
def addition(lst_d:list, key1:str, key2:str)->list: 
    """
    Crée une liste de dictionnaires de l'addition entre deux valeurs des dictionnaires.  
    lst_d est une liste de dictionnaires.
    key1 et key2 sont des clés des dictionnaires de la listes.
    """
    list_donnees = []
    for elem in lst_d:
        dico = {key1+" et "+key2: str(int(str_to_float(elem[key1]) + str_to_float(elem[key2])))} # Créé un dictionaire de l'addition entre la valeur attribué à key1 et à key2
        list_donnees.append(dico)

    return list_donnees

def medium(lst_d:list)->list: 
    """
    Crée une liste de dictionnaires de la moyenne entre toutes les valeurs d'un dictionnaire.
    lst_d est une liste de dictionnaires.
    """
    list_donnees = []
    for elem in lst_d: 
        #convertit la liste des nombres en nombres floattants en utilisant la fonction "str_to_float" definie plus haut
        elem_float = [str_to_float(i) for i in list(elem.values())] 
        dico = {"Moyenne": str(int(sum(list(elem_float))/len(list(elem_float))))} #ce qui permet de faire les calculs 
        list_donnees.append(dico)
    
    return list_donnees

def percentage(lst_d:list, key1:str, key2:str)->list:
    """
    Créé une liste de dictionnaires du pourcentage entre deux valeurs des dictionnaires.
    lst_d est une liste de dictionnaires.
    La valeur associée à key1 doit être une moyenne.
    key2 est une clé des dictionnaires de la liste. 
    """
    list_donnees = []
    for elem in lst_d:
        dico = {"Pourcentage de "+key1+" sur "+key2: str(int((str_to_float(elem[key1]) / str_to_float(elem[key2]))*100))+"%"}
        list_donnees.append(dico)

    return list_donnees

def rate_of_grow(lst_d:list, key1:str, key2:str)->list: 
    """
    Créé une liste de dictionnaires du calcul du taux de croissance entre deux valeurs des dictionnaires.
    lst_d est une liste de dictionnaires.
    key1 et key2 sont des clés des dictionnaires de la liste.
    """
    list_donnees = []
    for elem in lst_d:   
        try:  #  test si le deuxième élément de la liste est égal à 0 car on ne peut pas faire de division par zéro
            grow = int((str_to_float(elem[key1]) - str_to_float(elem[key2])))/str_to_float(elem[key2])
        except: 
            grow = 0 
        dico = {"Taux de croissance entre "+key1 +" et "+ key2: str(grow)}
        list_donnees.append(dico)

    return list_donnees

def prediction_growing(lst_d:list, key1:str, key2:str)->list: 
    """ 
    Créé une liste de prédictions à partir du taux de croissance (positionée en key1).
    lst_d est une liste de dictionnaires.
    """
    list_donnees = []
    for elem in lst_d:
        #Le taux de croissance étant un pourcentages il faut ajouter 1 avant de faire la mutiplication
        grow = 1 + str_to_float(elem[key1]) 
        dico = {"Prediction avec "+key1 : str(int(grow* str_to_float(elem[key2])))} 
        list_donnees.append(dico)

    return list_donnees


############### FONCTION SUR LES LISTES, DICTIONNAIRES, CSV ET HTML ###############


def change_value_list_dictionary(d_to_change, second_d, key1, key2)->None: 
    """
    Change la valeur associée à "key1" de d_to_change en la clé "key2" du second_d.
    d_to_change et second_d sont des listes de dictionnaires.
    """
     #zip() permet d'avoir une itération parallèle des deux listes de dictionnaires.
     #Les élements de d_to_change sont stockés dans elem_to_change et ceux de second_d dans elem
    for elem_to_change, elem in zip(d_to_change, second_d):
        elem_to_change[key1] = elem[key2]

def add_value_list_dictionary(d_to_change, second_d, key)->None: 
    """
    Ajoute la valeur associée à "key" de second_d aux dictionnaires de d_to_change.
    d_to_change et second_d sont des listes de dictionnaires.
    """
    for elem_to_add, elem in zip(d_to_change, second_d):
        elem_to_add[key] = elem[key]

def change_logement_value(d): #Fonction utile pour ne pas avoir à recopier plusieurs fois les mêmes lignes de code. 
    """
    Additionne les valeurs d'établissment et logements 
    Remplace la valeur de logement par cette addition
    """
    # Liste de dictionaire de l'addition des établissments et logements 
    logements_etablissement = csv2dict("nb_abonees-fibre_departement_trimestre", ['Logements', 'Ã‰tablissements']) 
    d_logements_etablissement = addition(logements_etablissement, "Logements", "Ã‰tablissements")

    #changement des valeurs dans le dictionaire
    change_value_list_dictionary(d, d_logements_etablissement, "Logements", "Logements et Ã‰tablissements")

def csv2dict(filename, header)->list:
    """
    Transforme un csv en dictionnaire.  
    filename est une chaine de caractères du nom de fichier csv. 
    header est une liste contenant les valeurs qui seront utilisées comme clé du dictionnaire sortie.
    """
    from os.path  import exists
    #permet de savoir si le csv existe bien 
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
    Transforme la liste de dictionaires "d" en un fichier csv.
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
    Créé un fichier html à partir d'un fichier csv. 
    h1_and_tbody est une variable contenant le titre du site et le header du tableau html
    """
    f = open(filename+".html", "w")
    htmlfile = '<!DOCTYPE html><html lang="fr-FR"><head><meta charset="utf-8"><title>SAE 15</title><link rel="stylesheet" href="style.css"></head><body>'+ h1_and_tbody 
    csvfile = open(filename+".csv", "r")
    csvreader = csv.reader(csvfile)

    for row in csvreader: #permet d'avoir le first_value = header (première ligne du csv)
        first_value = row[0]
        break

    for row in csvreader: #
        if row[0] == first_value: #permet de ne pas avoir ces valeurs écrites dans les tableaux
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
    Créé le csv nb_hab_avec_fibre_departements_annees
    """
    #Création d'une liste de dictionaires à partir du csv
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
    #Creéation d'une liste de dictionaires a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    # Création du dictionaire pour le calcul de la moyenne
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
    Créé le csv percentage_fibre_departement_annees.
    """
    #Création d'une liste de dictionaires a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    #Création du dictionaire pour le calcul de la moyenne
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
    Créé le csv prediction_fibre_departement.
    """
    #Création d'une liste de dictionaires à partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements', 'T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)
    change_logement_value(d)

    #Calcul le taux de croissance entre 2021 et 2022
    d_grow = rate_of_grow(d,'T3 2022', 'T3 2021')
    add_value_list_dictionary(d, d_grow, 'Taux de croissance entre T3 2022 et T3 2021')
    
    #Fait les prédictions pour 2023 en mutipliant le taux de croissance avec les valeurs de 2022
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
    print("Tous les fichiers ont bien été générés")