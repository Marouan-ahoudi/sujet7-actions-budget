import csv
from itertools import product


def charger_actions(chemin):
    actions = {}
    with open(chemin, newline="", encoding="utf-8") as f:
        for L in csv.DictReader(f):
            prerequis = {p for p in L["prerequis"].split("|") if p}
            actions[L["id"]] = {
                "cout": int(L["cout"]),
                "gain": int(L["gain"]),
                "prerequis": prerequis,
            }
    return actions

def verifier_prerequis_existent(actions):
    for id_, a in actions.items():
        inconnus = a["prerequis"] - set(actions)
        if inconnus:
            raise ValueError(f"Prérequis inconnu pour {id_} : {inconnus}")

def evaluer(selection, actions):
    ids = set(selection)
    for i in ids:
        if not actions[i]["prerequis"] <= ids:
            return None
    cout = sum(actions[i]["cout"] for i in ids)
    gain = sum(actions[i]["gain"] for i in ids)
    return cout, gain

def enumerer(actions, budget):
    ids = list(actions)
    for bits in product([0, 1], repeat=len(ids)):
        selection = [i for i, b in zip(ids, bits) if b]
        res = evaluer(selection, actions)
        if res is not None and res[0] <= budget:
            yield selection, res[0], res[1]

def meilleur_portefeuille(actions, budget):
    return max(enumerer(actions, budget), key=lambda s: (s[2], -s[1]))