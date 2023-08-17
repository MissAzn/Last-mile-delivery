import random
import copy
import time
import numpy as np

start = time.time()


# fonction qui retourne fitness d'un joueur
def fit(J, D):
    fitness = 0
    for i in range(len(J) - 1):
        fitness = fitness + D[J[i]][J[i + 1]]
    return fitness


# recherche local 2-opt
def deux_pt(J, D):
    start = time.time()
    global Joueur
    p = [J]
    for i in range(1, len(J) - 2):
        for j in range(i + 1, len(J)):
            if j - i == 1:
                pass
            Joueur = J[:]
            Joueur[i:j] = J[j - 1:i - 1:-1]
            if fit(Joueur, D) < fit(J, D):
                J = copy.deepcopy(Joueur)
                p.append(Joueur)
    #end_time = time.time()
    # Calculate the elapsed time
    #elapsed_time = end_time - start

    # Print the elapsed time
    #print(f"Elapsed time 2-opt {elapsed_time:.2f} seconds")

    return bestsol(p, D)


def swapping(J, D):
    j = copy.deepcopy(J)
    j.pop(0)
    j.pop(len(j) - 1)
    Joueur = copy.deepcopy(J)
    it = 0
    p = [J]
    while it < 6:
        it += 1
        r = random.choice(j)
        k = random.choice(j)
        if r == k:
            while r == k:
                r = random.choice(j)
                k = random.choice(j)
        x = Joueur.index(r)
        y = Joueur.index(k)
        Joueur[x] = k
        Joueur[y] = r
        if fit(Joueur, D) < fit(J, D):
            J = copy.deepcopy(Joueur)
            p.append(J)

    return bestsol(p, D)


def three_opt(J, D):
    start = time.time()
    it = 0
    Joueur = J
    p = [J]
    it += 1
    for i in range(1, len(J) - 3):
        for j in range(i + 2, len(J) - 1):
            for k in range(j + 2, len(J) - 1):
                # 3-opt
                # construire un nouveau joueur
                new = Joueur[:i + 1] + Joueur[i + 1:j + 1][::-1] + Joueur[j + 1:k + 1][::-1] + Joueur[k + 1:]
                if fit(new, D) < fit(Joueur, D):
                    Joueur = new
                    p.append(new)
    print('longueur de p est', len(p))
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start

    # Print the elapsed time
    print(f"Elapsed time 3OPT: {elapsed_time:.2f} seconds")

    return bestsol(p, D)


# Trop d'aléatoire dans cette fonction// à revoir les tournées ne vont pas etre réalisable
def v_insertion(Joueur, Joueur2, D):
    n = len(Joueur)
    indice = random.randint(1, n - 2)
    indexx = random.randint(1, n - 2)
    # select a random node
    node = Joueur[indice]
    y = Joueur2[indexx]
    Joueur2[indexx] = node
    x = Joueur2.index(node)
    Joueur2[x] = y

    if fit(Joueur2, D) < fit(Joueur, D):
        return Joueur2
    else:
        return Joueur

#pij recoit picap
def crossover(pij, picap):
    p1 = random.randint(1, len(pij)-6)
    p2 = random.randint(p1 + 1, len(pij) - 1)
    # pijp est le joueur pij apres l'entrainement personnalisé
    pijp = [0] * len(picap)
    for i in range(p1, p2):
        pijp[i] = pij[i]
    for i in range(1, p1):
        if picap[i] in pijp:
            x = picap[i]
            while x in pijp:
                x = random.choice(picap)
            pijp[i] = x
        else:
            pijp[i] = picap[i]
    for i in range(p2, len(pij) - 1):
        if picap[i] in pijp:
            x = picap[i]
            while x in pijp:
                x = random.choice(picap)
            pijp[i] = x
        else:
            pijp[i] = picap[i]
    return pijp


def teampower(team, D):
    power = 0
    for i in range(len(team)):
        power = power + fit(team[i], D)
    power = power / len(team)
    return power


# fonction qui retourne le capitaine d'équipe
def picapitain(team, D):
    fitness = []
    for i in range(len(team)):
        fitness.append(fit(team[i], D))
    ind = fitness.index(min(fitness))
    picap = team[ind]
    return picap


def match(team1, team2, D):
    goalteam1 = 0
    goalteam2 = 0
    for i in range(len(team1)):
        if fit(team1[i], D) < fit(team2[i], D):
            goalteam1 += 1
        elif fit(team2[i], D) < fit(team1[i], D):
            goalteam2 += 1
    # la fonction dois me retourner les points des équipes
    return goalteam1, goalteam2


# fonction qui ordonne les joueurs d'une équipe suivant un ordre décroissant de leurs fitness
def rank(team, D):
    team1 = []
    M = []
    for i in range(len(team)):
        M.append(fit(team[i], D))
    exist = True
    while exist:
        exist = False
        minn = min(M)
        ind = M.index(minn)
        team1.append(team[ind])
        M[ind] = 10000
        for j in range(len(M)):
            if M[j] != 10000:
                exist = True
                break
            else:
                continue
    # print(team1)
    return team1


# La taille de la population change ici
def rank1(pop, points):
    pop1 = []
    M = copy.deepcopy(points)
    for i in range(len(M)):
        maxx = max(M)
        ind = M.index(maxx)
        pop1.append(pop[ind])
        M[ind] = 0
    return pop1


# nearst neigbor
def nn(D):
    tour = [0]
    unvisited = [i for i in range(1, len(D))]
    current = random.choice(unvisited)
    unvisited.remove(current)
    tour.append(current)
    while unvisited:
        nearest_city = min(unvisited, key=lambda city: D[current][city])
        tour.append(nearest_city)
        current = nearest_city
        unvisited.remove(nearest_city)
    tour.append(0)
    return tour


# fonction qui retourne la meilleure solution d'une liste
def bestsol(list, D):
    M = []
    for i in range(len(list)):
        M.append(fit(list[i], D))
    ind = M.index(min(M))
    return list[ind]


class GB:
    def __init__(self, P, N, D):
        # nombre d'équipes dans la population
        self.picapt = 100000000000
        self.TQI = 100000000000
        self.pop = P
        self.distance = D
        # the actual population
        self.population = None
        self.joueur = N
        self.best = 100000000000

    def solution(self):
        population = []
        for j in range(self.pop):
            solution = []
            for k in range(self.joueur):
                s = nn(self.distance)
                solution.append(s)
            population.append(solution)
        return population

    # fonction qui affecte aléatoirement des coachs aux équipes
    def assign(self):
        coach = []
        for i in range(self.pop):
            x = random.randint(1, self.pop)
            while x in coach:
                x = random.randint(1, self.pop)
            coach.append(x)
        return coach

    # ici je dois entrer une population totalement ordonnée (ça va etre ordonnée selon le nombre de points des matchs)
    # le nombre d'équipes ne doit pas etre impair le nombre de joueurs aussi (probably)
    def transfert(self):
        N = self.pop / 2
        N = int(N)
        # i va s'arreter a 1
        j = 0
        for i in range(N):
            # premier joueur de la première population
            X = self.population[i][j]
            self.population[i][j] = self.population[self.pop - i - 1][self.joueur - j - 1]
            self.population[self.pop - i - 1][self.joueur - j - 1] = X
            j += 1
        return self.population

    # fonction qui retourne la meilleure solution d'une population et son fitness
    def BEST(self):
        best = []
        fitness = []
        for i in range(self.pop):
            x = picapitain(self.population[i], self.distance)
            best.append(x)
            fitness.append(fit(x, self.distance))
        minn = min(fitness)
        ind = fitness.index(minn)
        # retourner la meilleure solution du système ainsi que son fitness
        return best[ind], minn

    def season(self):
        # nombre d'itération à faire dans le crossover
        crossit =5
        essai = 5
        coach = self.assign()
        matrice = [[0 for i in range(12)] for j in range(4)]
        # pour chaque saison il en existe 2
        for k in range(2):
            teampoint = [0] * self.pop
            teamquality = [0] * self.pop
            for i in range(self.pop):
                for j in range(i + 1, self.pop):
                    S = [i, j]
                    # training
                    for x in S:
                        M = []
                        if coach[x] == 1:
                            for v in range(self.joueur):
                                # je retourne le premier joueur trapped in a local OPTIMUM
                                m = deux_pt(self.population[x][v], self.distance)
                                M.append(m)
                                if self.population[x][v] == m:
                                    matrice[x][v] += 1
                                    pij = m
                                    picap = picapitain(self.population[x], self.distance)
                                    indx = self.population[x].index(pij)
                                    # maintenant il faut faire du custom training
                                    p = [m]
                                    for z in range(crossit):
                                        l = crossover(picap, pij)
                                        p.append(l)
                                        if fit(l, self.distance) < fit(pij, self.distance):
                                            pij = l
                                    M[indx] = bestsol(p, self.distance)
                                    if M[indx] == m:
                                        matrice[x][v] += 1
                                if matrice[x][v] >= essai:
                                    r = x
                                    while r == x:
                                        r = random.randint(0, 3)
                                    inter = self.population[x][v]
                                    self.population[x][v] = self.population[r][v]
                                    self.population[r][v] = inter
                                    matrice[x][v] = 0
                            N = rank(M, self.distance)
                            self.population[x] = copy.deepcopy(N)
                        elif coach[x] == 2:
                            for v in range(self.joueur):
                                p = []
                                for ind in range(12):
                                    Joueur2 = random.choice(self.population[x])
                                    p.append(v_insertion(Joueur2, self.population[x][v], self.distance))
                                m = bestsol(p, self.distance)
                                M.append(m)
                                if self.population[x][v] == m:
                                    matrice[x][v] += 1
                                    pij = m
                                    picap = picapitain(self.population[x], self.distance)
                                    indx = self.population[x].index(pij)
                                    p = [m]
                                    for z in range(crossit):
                                        l = crossover(picap, pij)
                                        p.append(l)
                                        if fit(l, self.distance) < fit(pij, self.distance):
                                            pij = l
                                    M[indx] = bestsol(p, self.distance)
                                    if M[indx] == m:
                                        matrice[x][v] += 1
                                if matrice[x][v] >= essai:
                                    r = x
                                    while r == x:
                                        r = random.randint(0, 3)
                                    inter = self.population[x][v]
                                    self.population[x][v] = self.population[r][v]
                                    self.population[r][v] = inter
                                    matrice[x][v] = 0
                            N = rank(M, self.distance)
                            self.population[x] = copy.deepcopy(N)
                        elif coach[x] == 3:
                            for v in range(self.joueur):
                                m = swapping(self.population[x][v], self.distance)
                                M.append(m)
                                #print('avant', fit(self.population[x][v], self.distance), 'swapping',
                                      #fit(m, self.distance))
                                # if fit(self.population[x][v], self.distance) > fit(m, self.distance):
                                #           print('swapping yesss')
                                # si la solution n'a pas changé
                                if self.population[x][v] == m:
                                    pij = m
                                    matrice[x][v] += 1
                                    picap = picapitain(self.population[x], self.distance)
                                    indx = self.population[x].index(pij)
                                    p = [m]
                                    for z in range(crossit):
                                        l = crossover(picap, pij)
                                        p.append(l)
                                        if fit(l, self.distance) < fit(pij, self.distance):
                                            pij = l
                                    M[indx] = bestsol(p, self.distance)
                                    if M[indx] == m:
                                        matrice[x][v] += 1
                                if matrice[x][v] >= essai:
                                    r = x
                                    while r == x:
                                        r = random.randint(0, 3)
                                    inter = self.population[x][v]
                                    self.population[x][v] = self.population[r][v]
                                    self.population[r][v] = inter
                                    matrice[x][v] = 0
                                    # ordonner les joueurs de l'équipe x suivant un ordre décroissant de leur fitness
                            N = rank(M, self.distance)
                            self.population[x] = copy.deepcopy(N)

                        elif coach[x] == 4:
                            for v in range(self.joueur):
                                # vecteur des solutions
                                p = []
                                for ind in range(15):
                                    Joueur2 = random.choice(self.population[x])
                                    p.append(v_insertion(Joueur2, self.population[x][v], self.distance))
                                m = bestsol(p, self.distance)
                                #print('avant', fit(self.population[x][v], self.distance), 'v_insertion',
                                      #fit(m, self.distance))
                                M.append(m)
                                # si la solution n'a pas change
                                if self.population[x][v] == m:
                                    pij = m
                                    matrice[x][v] += 1
                                    picap = picapitain(self.population[x], self.distance)
                                    indx = self.population[x].index(pij)
                                    # maintenant il faut faire du custom training
                                    p = [m]
                                    for z in range(crossit):
                                        l = crossover(picap, pij)
                                        p.append(l)
                                        if fit(l, self.distance) < fit(pij, self.distance):
                                            pij = l
                                            p.append(l)
                                    M[indx] = bestsol(p, self.distance)
                                    if M[indx] == m:
                                        matrice[x][v] += 1
                                if matrice[x][v] >= essai:
                                    r = x
                                    while r == x:
                                        r = random.randint(0, 3)
                                    inter = self.population[x][v]
                                    self.population[x][v] = self.population[r][v]
                                    self.population[r][v] = inter
                                    matrice[x][v] = 0
                            # ordonner les joueurs de l'équipe x suivant un ordre décroissant de leur fitness
                            N = rank(M, self.distance)
                            self.population[x] = copy.deepcopy(N)
                        # Calculer la qualité de l'équipe
                        teamquality[x] = teampower(self.population[x], self.distance)
                        # teams power les ordonner aussi
                    # match day !!!!!!
                    S = match(self.population[i], self.population[j], self.distance)
                    if S[0] > S[1]:
                        # l'équipe "i" reçoit 3 points et l'équipe "j" reçoit 0
                        teampoint[i] = teampoint[i] + 3
                    elif S[0] == S[1]:
                        teampoint[i] = teampoint[i] + 1
                        teampoint[j] = teampoint[j] + 1
                    else:
                        teampoint[j] = teampoint[j] + 3
            # Ordonner la population selon les team points
            self.population = rank1(self.population, teampoint)
            self.population = self.transfert()

    def goldenball(self):
        # Initialisation de la solution aléatoire il faut mettre superieure ou égale dans notre cas
        self.population = self.solution()
        TQIP = 0
        for i in range(self.pop):
            TQIP = TQIP + teampower(self.population[i], self.distance)
        # sum des picap
        capitain = 0
        for i in range(self.pop):
            x = copy.deepcopy(picapitain(self.population[i], self.distance))
            capitain = capitain + fit(x, self.distance)
        y = self.BEST()
        bestp = y[1]
        #print('meilleur solution ', bestp)
        # La méthode peut commencer
        it = 0
        p = [y[0]]
        s = [bestp]
        while TQIP < self.TQI and bestp < self.best and capitain < self.picapt:
            it += 1
            #print("itération", it)
            # season
            self.season()
            self.TQI = TQIP
            self.best = bestp
            self.picapt = capitain
            TQIP = 0
            for i in range(self.pop):
                TQIP = TQIP + teampower(self.population[i], self.distance)
            # sum des picap
            capitain = 0
            for i in range(self.pop):
                x = picapitain(self.population[i], self.distance)
                capitain = capitain + fit(x, self.distance)
            y = self.BEST()
            bestp = y[1]
            #print("La meilleur solution trouvée a l'itération", it, "est", y[0])
            #print("son fitness est ", y[1])
            p.append(y[0])
            s.append(y[1])
        indd = s.index(min(s))
        #print("La meilleur solution trouvée est ", p[indd])
        #print("son fitness est ", s[indd])
        return p[indd], s[indd]


# Generate upper triangle of the matrix
triangle = [[random.randint(1, 10) for j in range(i + 1, 10)] for i in range(10)]

# Create a symmetric matrix by copying upper triangle to lower triangle
D = [[0 for j in range(10)] for i in range(10)]
for i in range(10):
    for j in range(i, 10):
        if i == j:
            D[i][j] = 0
        else:
            D[i][j] = triangle[i][j - i - 1]
            D[j][i] = D[i][j]
# print(D)

P = 4
N = 12

# G: GB = GB(P, N, D)
# G.goldenball()

end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start

# Print the elapsed time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
