import streamlit as st
import random
import math
import pandas as pd
import base64

# Define your optimization functions here...

def vecteur_site(offre, capacites, matrice_distance):
    vecteur_resultant = []
    for i, cap_site in enumerate(offre):
        vecteur_site = []
        for j, cap_poste in enumerate(capacites):
            if cap_poste >= cap_site and matrice_distance[i][j] <= 30:
                vecteur_site.append(j + 1)  # Ajouter l'indice du poste en commençant par 1
            else:
                vecteur_site.append(-1)  # Ajouter -1 si non raccordable
        vecteur_resultant.append(vecteur_site)
    return vecteur_resultant

def shuffle(vecteurs_sites):
    vecteurs_sites_ameliore = []
    for vecteur_site in vecteurs_sites:
        random.shuffle(vecteur_site)  # Mélanger l'ordre des valeurs dans chaque vecteur
        vecteurs_sites_ameliore.append(vecteur_site)
    return vecteurs_sites_ameliore

def creation_solution(vecteur_resultant, offre, capacites, demande):
    solution = []
    capacites_restantes = capacites[:]  # Copie des capacités
    demande_restante = demande
    for i, vecteur in enumerate(vecteur_resultant):
        site_assigne = False
        for site in vecteur:
            if site != -1 and capacites_restantes[site - 1] >= offre[i]:
                solution.append(site)
                capacites_restantes[site - 1] -= offre[i]
                demande_restante -= offre[i]
                site_assigne = True
                break
        if not site_assigne:
            solution.append(-1)  # Aucun site valide trouvé ou capacité insuffisante
    return solution, capacites_restantes, demande_restante

def fitness(solution, matrice_distance):
    fitness_value = 0
    for i, site in enumerate(solution):
        if site != -1 and site != 0 :
            fitness_value += matrice_distance[i][site - 1]
    return fitness_value

def mise_a_jour(solution1, solution2, matrice_distance):
    fitness1 = fitness(solution1, matrice_distance)
    fitness2 = fitness(solution2, matrice_distance)
    
    if fitness2 < fitness1:
        return solution2, fitness2
    else:
        return solution1, fitness1

def rectification(offre, capacites_restantes, solution, demande_restante):
    while demande_restante < 0:
        min_offre_index = -1
        min_offre_value = float('inf')
        for i, o in enumerate(offre):
            if o > 0 and o < min_offre_value and solution[i] != -1 and solution[i] != 0:
                min_offre_index = i
                min_offre_value = o

        if min_offre_index == -1:  # Si aucun site valide n'est trouvé
            break

        poste_index = solution[min_offre_index] - 1  # Indice du poste actuellement assigné

        if abs(demande_restante) <= min_offre_value:
            # Si la demande restante peut être couverte par l'offre minimale
            offre[min_offre_index] -= abs(demande_restante)  # Ajuster l'offre du site
            capacites_restantes[poste_index] += abs(demande_restante)  # Restaurer la capacité utilisée au poste
            demande_restante += abs(demande_restante)  # Mettre à jour la demande restante à 0
            if offre[min_offre_index] == 0:
                solution[min_offre_index] = 0  # Désactiver ce site dans la solution
        else:
            # Si la demande restante est supérieure à l'offre minimale
            offre[min_offre_index] = 0  # Effacer l'offre du site désactivé pour éviter sa réutilisation
            capacites_restantes[poste_index] += min_offre_value  # Restaurer toute la capacité utilisée
            demande_restante += min_offre_value  # Réduire la demande restante
            solution[min_offre_index] = 0  # Désactiver ce site

    return offre, capacites_restantes, solution, demande_restante

def get_table_download_link(df):
    """Génère un lien permettant de télécharger les données d'un dataframe pandas sous forme de fichier CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Contournement de l'écriture CSV interne de pandas
    href = f'<a href="data:file/csv;base64,{b64}" download="optimization_results.csv">Télécharger le fichier CSV</a>'
    return href

# Interface utilisateur Streamlit
st.title("Optimisation de l'Allocation des Ressources")

# Barre latérale pour les paramètres d'entrée
st.sidebar.header("Paramètres d'Entrée")

# Upload files for sites and posts
sites_file = st.sidebar.file_uploader("Uploader le fichier des sites (Excel)", type=["xlsx"])
posts_file = st.sidebar.file_uploader("Uploader le fichier des postes (Excel)", type=["xlsx"])
if sites_file is not None:
    sites_data = pd.read_excel(sites_file)

    # Remove rows with any None values in any column
    sites_data_cleaned = sites_data.dropna()

    st.write("Data from Sites file (after removing rows with None values):")
    st.write(sites_data_cleaned)

if posts_file is not None:
    posts_data = pd.read_excel(posts_file)
    posts_data_cleaned = posts_data.dropna()
    st.write("Data from Posts file:")
    st.write(posts_data)

# Input fields for demand, initial rate, and final rate
demande = st.sidebar.number_input("Demande", min_value=0)
taux_initial = st.sidebar.number_input("Taux Initial", min_value=0, value=5)
taux_final = st.sidebar.number_input("Taux Final", min_value=0, value=4)

# Entrée de texte pour le nombre d'itérations
nbr_iterations = st.sidebar.number_input("Nombre d'Itérations", min_value=1, value=5)

# Bouton pour démarrer l'optimisation
if st.sidebar.button("Démarrer l'Optimisation"):
    if sites_file is not None and posts_file is not None:
        # Read data from uploaded Excel files
        sites_df = sites_data_cleaned
        posts_df = posts_data_cleaned

        # Extract data from dataframes
        sites = sites_df['sites'].tolist()
        print(sites)
        offre = sites_df['offre'].tolist()
        print(offre)
        postes=posts_df['Postes'].tolist()
        capacites = posts_df['capacités'].tolist()

        donnees = list(zip(postes, capacites))
        # Définir les dimensions de la matrice
        nb_lignes = len(offre)
        nb_colonnes = len(capacites)
        matrice_distance = [[random.randint(10, 50) for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

        # Initialisation des variables pour la boucle
        alpha = random.uniform(0.8, 0.99)
        taux = taux_initial

        # Liste pour stocker toutes les solutions parcourues
        solutions_parcourues = []

        # Calcul des vecteurs de sites et création de la solution initiale
        vecteurs_sites = vecteur_site(offre, capacites, matrice_distance)
        solution_initiale, capacites_restantes_init, demande_restante_init = creation_solution(vecteurs_sites, offre, capacites, demande)

        # Calcul de la fitness de la solution initiale
        fitness_initiale = fitness(solution_initiale, matrice_distance)

        # Initialisation de la meilleure solution et de la meilleure fitness
        best_solution = solution_initiale
        best_fitness = fitness_initiale

        while taux > taux_final:
            for i in range(nbr_iterations):
                vecteurs_sites_ameliore = shuffle(vecteurs_sites)

                nouvelle_solution, capacites_restantes_amel, demande_restante_amel = creation_solution(vecteurs_sites_ameliore, offre, capacites, demande)

                if demande_restante_amel < 0:
                    offre_modifiee, capacites_restantes_amel, nouvelle_solution, demande_restante_amel = rectification(
                        offre.copy(), capacites_restantes_amel.copy(), nouvelle_solution.copy(), demande_restante_amel
                    )

                nouvelle_fitness = fitness(nouvelle_solution, matrice_distance)

                solutions_parcourues.append((nouvelle_solution, nouvelle_fitness))

                delta_fitness = nouvelle_fitness - fitness_initiale

                if delta_fitness <= 0:
                    best_solution, best_fitness = mise_a_jour(best_solution, nouvelle_solution, matrice_distance)
                    vecteurs_sites = vecteurs_sites_ameliore
                else:
                    p = random.uniform(0, 1)
                    if 0 <= p <= math.exp(-delta_fitness / taux):
                        best_solution, best_fitness = mise_a_jour(best_solution, nouvelle_solution, matrice_distance)
                        vecteurs_sites = vecteurs_sites_ameliore

            taux *= alpha

        # Afficher la meilleure solution et la meilleure fitness
        st.header("Meilleure Solution Trouvée")
        st.write("Solution:", best_solution)
        st.write("Fitness:", best_fitness)

        # Afficher les solutions explorées
        st.header("Solutions Explorées")
        for i, (solution, fitness) in enumerate(solutions_parcourues):
            st.write(f"Itération {i+1}: Solution - {solution}, Fitness - {fitness}")

        # Sauvegarder les données au format CSV
        df = pd.DataFrame({
            "Sites": sites,
            "Offre": offre,
            "Meilleure Solution": best_solution
        })
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

    else:
        st.error("Veuillez uploader les fichiers des sites et des postes.")

# Display additional information or results here...
