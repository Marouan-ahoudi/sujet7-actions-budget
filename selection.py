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