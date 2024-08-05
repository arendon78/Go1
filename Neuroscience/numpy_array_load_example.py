import numpy as np

# Exemple de tableau NumPy
tableau_numpy = np.array([1, 2, 3, 4, 6])

# Sauvegarde du tableau NumPy
np.save('tableau.npyy', tableau_numpy)

try : 
    # Chargement du tableau NumPy
    tableau_numpy_charge = np.load('tableau.npyyy')
    print(tableau_numpy_charge)

except FileNotFoundError :
    print("FileNotFoundError : numpy array not saved yet.")