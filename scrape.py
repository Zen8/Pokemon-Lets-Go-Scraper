import requests, html.parser, re, time
from bs4 import BeautifulSoup
import pprint as pp

def sortLocations(poke):
    locations = []
    if poke != []:
        poke = poke[16:]
        i, buffer = 1, []
        for line in poke:
            buffer.append(line)
            if i == 6:
                i = 1
                location = re.match("<a.*>(.*)</a>", buffer[1])
                type = re.match("<td.*>(.*)</td>", buffer[2])
                chance = re.match("<td.*>(.*)</td>", buffer[3])
                if chance.group(1).strip() == "%":
                    chance = "Rare Spawn"
                else:
                    chance = chance.group(1).strip()
                locations.append(location.group(1).strip() + " - " + type.group(1).strip().split()[-1] + " - " + chance)
                buffer = []
            else:
                i += 1
    return locations

def getPokeName(data):
    pass

def getPokemonData(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    extractData = soup.findAll("table", class_ = "dextable")
    pikachu, eevee, locationsP, locationsE = [], [], {}, {}
    pokemonName = re.match("<td.*>(.*)</td>", str(extractData[0]).split("\n")[10])

    if len(extractData) > 0:
        for i in range(len(extractData)):
            data = str(extractData[i]).split("\n")
            if "pikachu" in data[0].lower():
                pikachu = data
            if "eevee" in data[0].lower():
                eevee = data

    locationsP = sortLocations(pikachu)
    locationsE = sortLocations(eevee)

    return locationsP, locationsE, pokemonName.group(1)

for i in range(1, 152):
    if i < 10:
        dexNo = "00" + str(i)
    elif i < 100:
        dexNo = "0" + str(i)
    else:
        dexNo = str(i)

    print(dexNo)
    url = "https://www.serebii.net/pokedex-sm/location/{}.shtml#letsgoe".format(dexNo)
    locationsP, locationsE, pokemonName = getPokemonData(url)

    locationsP = "Uncatchable" if locationsP == [] else ",".join(locationsP)
    locationsE = "Uncatchable" if locationsE == [] else ",".join(locationsE)

    with open("data/Pikachu/pokemon.txt", "a") as f:
        f.write("{},{},{}\n".format(dexNo, pokemonName, locationsP))
    with open("data/Eevee/pokemon.txt", "a") as f:
        f.write("{},{},{}\n".format(dexNo, pokemonName, locationsE))
    time.sleep(0.75)
