import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from main import *
from kmeanss import *
import pandas as pd
from ACO1 import *
from routingpy import Graphhopper, ORS, MapboxOSRM
from shapely.geometry import Polygon
import folium
from graphh import GraphHopper

# Define the clients and their profile parameter
api = Graphhopper(api_key='1aa1a627-b57d-47c3-8080-b220ca570e7c'), 'car'

geolocator = Nominatim(user_agent="my_application")


def reverse_geocode(latitude, longitude):
    location = None
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
    except GeocoderTimedOut:
        return reverse_geocode(latitude, longitude)
    if location:
        return location.address
    else:
        return None


# FONCTION GEOPY POUR COVERTIR LES CORDONNEES POLAIRE en quartiers : Reverse
# matrice de distance de chaque cluster
def matrice_kmeans(c, clusters):
    matrices = []
    for i in range(len(clusters)):
        c1 = [[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
        for j in range(len(clusters[i])):
            for k in range(len(clusters[i])):
                c1[j][k] = c[clusters[i][j]][clusters[i][k]]
        matrices.append(c1)
    return matrices


# Si je veux ajouter l'option des quartiers il faut ajouter le vecteur demande en paramètre
def zones(file_path, capacite):
    Qj = capacite
    df = pd.read_excel(file_path)

    latitude = df['Latitude:']
    longitude = df['Longitude:']
    adresse1 = df['adresse']
    n = len(df)
    adresse = []
    for i in range(n):
        adresse.append(adresse1[i])
    plt.scatter(longitude, latitude)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # plt.show()

    r = []
    # vecter des demande
    for i in range(n):
        # r.append(random.randint(1, 5))
        if i == 0:
            r.append(0)
        else:
            r.append(1)
    # sauvegarder l'indice de la station
    # vecteur des sommets
    xy = []
    for i in range(len(df)):
        xy.append([latitude[i], longitude[i]])
    # l'indice de l'emplacement de la station

    # Sauvegarde des coordonnées polaires de la station
    station = xy[0]
    # mettre la station en position 0
    #print('cordonnées de la station', station)
    distance = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            distance[i][j] = geodesic(xy[i], xy[j]).km

    r1 = []
    for i in range(n):
        r1.append(r[i])
    # print("r = ", r)
    # il faut revoir la valeur de k
    k = int(sum(r) / Qj) + 1
    # Je dois retourner le k aussi
    #print("k = ", k)
    ind = [i for i in range(n)]
    ind = ordre_decroissant(r1, n, ind)
    # print(ind)
    D = [ind[i] for i in range(k)]
    R = [ind[i] for i in range(k, n)]
    klusters = clustering(n, k, Qj, D, R, r, xy)
    clusters = convergence(n, k, Qj, D, R, r, xy, klusters)

    return clusters, distance, k, adresse


# cette fonction retourne toutes les solutions
def Tournée(clusters, c, adresse):
    for i in range(len(clusters)):
        if 0 not in clusters[i]:
            clusters[i].append(0)
    Distance = matrice_kmeans(c, clusters)
    Solutions = []
    M = []
    for i in range(len(clusters)):
        # print('cluster', i, 'est ', clusters[i])
        # print('Voici la matrice des distance', Distance[i])
        G: GB = GB(P, N, Distance[i])
        y = G.goldenball()
        m = [0]
        clusters[i].remove(0)
        for j in range(len(clusters[i])):
            m.append(clusters[i][j])
        m.append(0)
        M.append(m)
        S = [adresse[0]]
        for j in range(1, len(m) - 1):
            S.append(adresse[m[y[0][j]]])
        S.append(adresse[0])
        #print('this is s', S)
        # Append le fitness de chaque solution
        S.append(y[1])
        Solutions.append(S)
        #print("solution du cluster", i, "est", S)
        #print("______________________________________________________")
    return Solutions


# ajoute le M

def tournee_ACO(clusters, c, addresse):
    n = len(clusters)
    for i in clusters:
        if 0 not in i:
            i.append(0)
    Q = 1
    p = 0.1
    N = 3
    q0 = 0.9
    alpha = 0.1
    beta = 2
    Tournees = []
    for i in range(len(clusters)):
        d = [[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
        toij1 = [[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
        for j in range(len(clusters[i])):
            for k in range(len(clusters[i])):
                d[j][k] = c[clusters[i][j]][clusters[i][k]]
        Lnn = NN(len(clusters[i]), d)
        for j in range(len(clusters[i])):
            for k in range(len(clusters[i])):
                toij1[j][k] = 1 / (n * Lnn)
        nij1 = inverse(len(clusters[i]), d)
        Solutions = colonie_de_fourmis(len(clusters[i]), toij1, nij1, alpha, beta, d, 3, q0, N, Q, p)
        Tournee_cluster = []
        for j in range(len(Solutions)):
            Tournee_cluster.append(clusters[i][Solutions[j]])
        Tournees.append(Tournee_cluster)
    T = []
    for h in range(len(Tournees)):
        if Tournees[h][0] != 0:
            j = Tournees[h].index(0)
            a = Tournees[h][j:len(Tournees[h])] + Tournees[h][1:j]
            a.append(0)
            T.append(a)
        else:
            T.append(Tournees[h])

    Distances = []
    for i in T:
        s = 0
        for j in range(len(i) - 1):
            s = s + c[i[j]][i[j + 1]]
        Distances.append(s)

    Itineraires = []
    for i in range(len(T)):
        Itineraire = []
        for j in range(len(T[i])):
            Itineraire.append(addresse[T[i][j]])
        Itineraires.append(Itineraire)
    for i in range(len(T)):
        Itineraires[i].append(Distances[i])
    for i in range(len(T)):
        print("La tournée: ", Itineraires[i])
        print("La distance: ", Distances[i])
        print("________________________________________")

    return Itineraires


# tester sur une instance
file = 'Data Alger EST Final.xlsx'
#cap = 10
df = pd.read_excel(file)
latitude = df['Latitude:']
longitude = df['Longitude:']
adresse = df['adresse']
#print(df)

#clusters, D, K, adress = zones(file, cap)
# print('clusters', clusters)
# print(Tournée(clusters, D, adress))
#M = tournee_ACO(clusters, D, adress)


# plt.scatter(longitude, latitude)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()
# for i in range(len(latitude)):
# adresse.append(reverse_geocode(latitude[i], longitude[i]))
# df fait reference a  data frame
# df['adresse'] = adresse
# df.to_excel(file, index=False)
# print(df.head)
# print('indice de station',adresse[0])

# for j in range(len(Coordonnees_des_tournees)):
# display(m[j])
