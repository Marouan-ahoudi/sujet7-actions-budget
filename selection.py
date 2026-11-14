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

import matplotlib.pyplot as plt

def courbe_sensibilite(actions, budget_max=20):
    budgets = list(range(budget_max + 1))
    gains = [meilleur_portefeuille(actions, b)[2] for b in budgets]
    return budgets, gains


def tracer(budgets, gains, fichier="budget_sensibilite.png"):
    plt.step(budgets, gains, where="post", marker="o")
    plt.xlabel("Budget")
    plt.ylabel("Meilleur bénéfice")
    plt.title("Budget disponible et bénéfice maximal")
    plt.grid(alpha=0.3)
    plt.savefig(fichier, dpi=150)
    plt.close()

def tests():
    actions = charger_actions("actions.csv")
    verifier_prerequis_existent(actions)

    sel, cout, gain = meilleur_portefeuille(actions, 10)
    assert set(sel) == {"C", "D", "F"} and cout == 9 and gain == 15

    assert meilleur_portefeuille(actions, 0)[0] == []

    for s, _, _ in enumerer(actions, 20):
        assert "D" not in s or "C" in s

    _, gains = courbe_sensibilite(actions)
    assert all(a <= b for a, b in zip(gains, gains[1:]))

    try:
        verifier_prerequis_existent({"X": {"cout": 1, "gain": 1, "prerequis": {"Z"}}})
        assert False, "ValueError attendue"
    except ValueError:
        pass

    print("Toutes les vérifications passent")