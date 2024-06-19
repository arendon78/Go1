from itertools import product

def combinations():

    N_REPEAT = 4
    # La liste des nombres
    numbers = [
        0,
        36.101083032490976,
        45.045045045045036,
        59.880239520958085,
        90.09009009009007
    ]

    # Générer toutes les combinaisons possibles de 6 nombres (avec répétition)
    comb_of_six_with_repetition = list(product(numbers, repeat=N_REPEAT))

    # Ensemble pour stocker les résultats et leurs triplés sans doublon
    results_with_triples = set()

    # Générer toutes les combinaisons de + et - (2^6 = 64 combinaisons)
    sign_combinations = list(product([1, -1], repeat=N_REPEAT))

    # Parcourir chaque combinaison de six nombres avec répétition
    for combo in comb_of_six_with_repetition:
        # Pour chaque combinaison de signes, appliquer les signes aux nombres
        for signs in sign_combinations:
            # Calculer la somme pondérée par les signes
            number = sum(sign * num for sign, num in zip(signs, combo))

            # Construire le triplé avec les signes appliqués
            operation_triple = tuple(sign * num for sign, num in zip(signs, combo))

            # Ajouter le résultat et le triplé à l'ensemble
            results_with_triples.add((number, operation_triple))

    # Convertir l'ensemble en une liste triée des résultats avec leurs triplés
    sorted_results_with_triples = sorted(results_with_triples)

    # Optionnel: Afficher tous les nombres possibles avec leurs triplés correspondants
    # for result, triple in sorted_results_with_triples:
        # print(f"{result} = {triple}")

    # Extraire uniquement les résultats triés
    # sorted_results_only = sorted(result for result, _ in sorted_results_with_triples)

    # Retourner la liste des résultats triés
    # for j in sorted_results_only:s
        # print(j)

    #normalize
    results = []
    [results.append(r) for r,_ in results_with_triples ]
    m = max(results)
    l=list(results_with_triples)
    lprime = []

    for i in range(len(l)):
        lprime.append((l[i][0]/m,l[i][1]))

    return lprime


print(combinations())



