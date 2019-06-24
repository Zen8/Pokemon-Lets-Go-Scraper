import pprint as pp
from copy import deepcopy

def doStuff(data):
    newData = {}
    for i in data:
        newData[i] = {}
        for j in data[i]:
            newData[i][j] = []
            if data[i][j][0] == 'Uncatchable':
                newData[i][j].append('Uncatchable')
            else:
                for k in data[i][j]:
                    components = k.split(" - ")
                    if len(components) > 3:
                        components = [" ".join(components[:-2])] + components[-2:]
                    if components[1].lower() == "grass":
                        pass
                    elif components[1].lower() == "sky":
                        pass
                    elif components[1].lower() == "spawns":
                        pass
                    newData[i][j].append(components)
    finalData = {}
    for i in newData:
        finalData[i] = {}
        for j in newData[i]:
            finalData[i][j] = []
            for k in newData[i][j]:
                if finalData[i][j] == []:
                    if k == "Uncatchable":
                        finalData[i][j] = ["Uncatchable"]
                        continue
                    if k[-1] == "Rare Spawn":
                        finalData[i][j] = [",".join([k[0]] + [k[-1]])]
                        continue
                    if k[-2] == "Grass" or k[-2] == "Sky" or k[-2] == "Water":
                        finalData[i][j].append([",".join(k[:-1]), k[-1]])
                else:
                    if k[-2] == "Grass" or k[-2] == "Sky" or k[-2] == "Water":
                        finalData[i][j].append([",".join(k[:-1]), k[-1]])
    for i in finalData:
        for j in finalData[i]:
            if len(finalData[i][j]) > 1:
                max, maxIndex = 0, -1
                for ki, k in enumerate(finalData[i][j]):
                    if len(k) > 5:
                        continue
                    if int(k[-1][:-1]) > max:
                        maxIndex = ki
                        max = int(k[-1][:-1])
                finalData[i][j] = [finalData[i][j][maxIndex]]
    #pp.pprint(finalData)
    for i in finalData:
        key = list(finalData[i].keys())[0]
        finalData[i][key] = listRemover(list(finalData[i].values()))

    return finalData

def listRemover(data):
    while type(data) == type([]):
        if type(data[0]) == type([]):
            data = data[0]
        elif len(data) == 1:
            data = data[0]
        else:
            data = data[0] + "," + data[1]
    return data

dataP, dataE = {}, {}

with open("data/Pikachu/pokemon.txt") as f:
    for line in f:
        line = line.strip().split(",")
        dataP[line[0]] = {line[1] : [i for i in line[2:]]}

with open("data/Eevee/pokemon.txt") as f:
    for line in f:
        line = line.strip().split(",")
        dataE[line[0]] = {line[1] : [i for i in line[2:]]}

dataP, dataE = doStuff(dataP), doStuff(dataE)

with open("data/Pikachu/csvpokemon.txt", "a") as f:
    for i,t in enumerate(dataP.items()):
        name = list(t[1].keys())[0]
        location = list(t[1].values())[0]
        f.write("{},{}\n".format(name, location))
