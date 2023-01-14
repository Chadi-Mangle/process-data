import csv

############### FONCTION UTILITAIRE ###############

def fixed(): 
    from os import listdir

    csvlist = listdir("./")
    for elem in csvlist: 
        if elem[len(elem)-4:] == ".csv": 
            f = open(elem, "r")
            text = f.read().replace("\n\n", "\n")
            f = open(elem, "w")
            f.write(text)
            f.close()

def str_to_float(str:str)->float: # "str:str"   permet de dire que la variable str est une chaine de caractère 
    try: 
        return float(str.replace(",", '.')) #permet de pas avoir de problème lors de la conversion en entier ou floant des données de n'importe quel base de donnée
    except: 
        return str

############### FONCTION DE CALCUL ###############

def addition(lst_d:list, key1:str, key2:str)->list: # "lst_d:list" permet de savoir que lst_d esr une list. "key1:str, key2:str" et que key1 et key2 sont des chaines de caractères
    list_donnees = []
    for elem in lst_d:
        dico = {key1+" et "+key2: str(int(str_to_float(elem[key1]) + str_to_float(elem[key2])))} # Créé un dictionaire de l'addition entre la valeur attribué à key1 et à key2
        list_donnees.append(dico)

    return list_donnees

def medium(lst_d:list)->list: 
    list_donnees = []
    for elem in lst_d: 
        elem_float = [str_to_float(i) for i in list(elem.values())] #converti la liste des nombres en nombres floatant en utilisant la fonction "str_to_float" definie plus haut
        dico = {"Moyenne": str(int(sum(list(elem_float))/len(list(elem_float))))} #ce qui permet de faire les calculs 
        list_donnees.append(dico)
    
    return list_donnees

def percentage(lst_d:list, key1:str, key2:str)->list: 
    list_donnees = []
    for elem in lst_d:
        dico = {"Pourcentage de "+key1+" sur "+key2: str(int((str_to_float(elem[key1]) / str_to_float(elem[key2]))*100))+"%"}
        list_donnees.append(dico)

    return list_donnees

def rate_of_grow(lst_d:list, key1:str, key2:str)->list: #calcul le taux de croissance
    list_donnees = []
    for elem in lst_d:   
        try:  #  test si le deuxième element de la liste est égale à 0 car on ne peut pas faire de division par zéro
            grow = int((str_to_float(elem[key1]) - str_to_float(elem[key2])))/str_to_float(elem[key2])
        except: 
            grow = 0 
        dico = {"Taux de croissance entre "+key1 +" et "+ key2: str(grow)}
        list_donnees.append(dico)

    return list_donnees

def prediction_growing(lst_d:list, key1:str, key2:str)->list: #la fonction prédit a partir du taux de croissances (possitioné en key2)
    list_donnees = []
    for elem in lst_d:
        grow = 1 + str_to_float(elem[key1]) 
        dico = {"Prediction avec "+key1 : str(int(grow* str_to_float(elem[key2])))} #
        list_donnees.append(dico)

    return list_donnees
 
############### FONCTION SUR LES LISTE, DICTIONNAIRE, CSV ET HTML ###############

def change_value_list_dictionary(d_to_change, second_d, key1, key2)->None: 
    for elem_to_change, elem in zip(d_to_change, second_d): #
        elem_to_change[key1] = elem[key2]

def add_value_list_dictionary(d_to_change, second_d, key)->None: 
    for elem_to_change, elem in zip(d_to_change, second_d): #
        elem_to_change[key] = elem[key]

def change_logement_value(d):
    # Liste de dictionaire de l'addition des établisments et logements 
    logements_etablissement = csv2dict("nb_abonees-fibre_departement_trimestre", ['Logements', 'Ã‰tablissements']) 
    d_logements_etablissement = addition(logements_etablissement, "Logements", "Ã‰tablissements")

    #changement des valeurs dans le dictionaire
    change_value_list_dictionary(d, d_logements_etablissement, "Logements", "Logements et Ã‰tablissements")

def csv2dict(filename, header)->None: # transforme un csv en dictionaire 
    list_donnees_csv = []
    f = open(filename+".csv", "r")
    csvreader = csv.DictReader(f, delimiter=";")
    for row in csvreader:
        dico = {}
        for elem in header: 
            dico[elem] = row[elem]
        list_donnees_csv.append(dico)
    return list_donnees_csv

def dict2csv(d:list, filename:str)->None: #transforme dictionaire en csv  
    csvfile = open(filename+".csv" , "w")
    fieldnames = d[0].keys() 
    writer = csv.DictWriter(csvfile ,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(d)
    csvfile.close()
    fixed()

def csv2html(filename:str, h1_and_tbody:str)->None: #transforme un csv en html
    f = open(filename+".html", "w")
    htmlfile = '<!DOCTYPE html><html lang="fr-FR"><head><meta charset="utf-8"><title>SAE 15</title><link rel="stylesheet" href="style.css"></head><body>'+ h1_and_tbody 
    csvfile = open(filename+".csv", "r")
    csvreader = csv.reader(csvfile)

    for row in csvreader: # 
        first_value = row[0]
        break

    for row in csvreader: #
        if row[0] == first_value:
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
    #Creéation d'une liste de dictionaire a partir du csv
    header = ['Code dÃ©partement', 'Nom dÃ©partement', 'Logements', 'T4 2017', 'T3 2018', 'T3 2019', 'T3 2020', 'T3 2021', 'T3 2022']
    d= csv2dict("nb_abonees-fibre_departement_trimestre", header)

    change_logement_value(d)

    #création du nouveau csv et html
    dict2csv(d, "nb_abonees-fibre_departement_annees")
    csv2html("nb_abonees-fibre_departement_annees", '<h1>Nombre d\'habitation possÃ©dant la fibre par dÃ©partements et par annÃ©es.</h1><div><table><thead><tr><th>Code du dÃ©partements</th><th>Nom du dÃ©partements</th><th>Nombre d\'habitation</th><th>Logement avec la fibre en 2017</th><th>Logement avec la fibre en 2018</th><th>Logement avec la fibre en 2019</th><th>Logement avec la fibre en 2020</th><th>Logement avec la fibre en 2021</th><th>Logement avec la fibre en 2022</th></thead><tbody>')

def moy_fibre_departement_annees(): 
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


if __name__ == "__main__": 
    nb_hab_avec_fibre_departements_annees()
    moy_fibre_departement_annees()
    percentage_fibre_departement_annees()
    prediction_fibre_departement()
    print("Tous les fichiers ont bien été généré")