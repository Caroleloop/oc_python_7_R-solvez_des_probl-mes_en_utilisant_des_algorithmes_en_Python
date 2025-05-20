import csv
from itertools import combinations
import time

# Link to file
file_path = "C:/Formation/Projet_07/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

# budget max
MAX_BUDGET = 500


# Load CSV file into a list
def load_file(filename):
    actions = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cost = float(row["Coût par action (en euros)"])
                profit_percent = float(row["Bénéfice (après 2 ans)"].replace("%", ""))
                if cost > 0 and profit_percent > 0:
                    actions.append({"name": row["Actions #"], "cost": cost, "profit": profit_percent})
            except ValueError:
                continue
    return actions


# Calculation of share profit
def profit_calculation(actions):
    for action in actions:
        if action["cost"] > 0 and action["profit"] > 0:
            action["profit_value"] = (float(action["cost"])) * (((float(action["profit"])))) / 100


def find_best_combination(actions):
    best_profit = 0
    best_combination = []
    for i in range(1, len(actions) + 1):
        for combo in combinations(actions, i):
            total_cost = sum(a["cost"] for a in combo)
            if total_cost <= MAX_BUDGET:
                total_profit = sum(a["profit_value"] for a in combo)
                if total_profit > best_profit:
                    best_profit = total_profit
                    best_combination = combo
    return best_combination, best_profit


if __name__ == "__main__":
    start = time.time()
    actions = load_file(file_path)
    profit_calculation(actions)
    best_combination, best_profit = find_best_combination(actions)
    print("Meilleure combinaison d’actions :")
    for action in best_combination:
        print(f"{action['name']} - Coût : {action['cost']} € - Bénéfice : {action['profit_value']:.2f} €")
    print(f"\nProfit total : {best_profit:.2f} €")
    end = time.time()
    print(f"Temps d'exécution : {end - start:.2f} secondes")
