import csv
import time

# Fichier CSV
file_path = "C:/Formation/Projet_07/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

# Budget maximal en euros
MAX_BUDGET = 500


def load_data(filename):
    """
    Loads data from a CSV file containing shares.

    Each valid line in the file must contain a cost and a benefit (in percent).
    Lines with invalid data (non-numeric or negative values) are ignored.

    Args:
        filename (str): Path to CSV file to be loaded.

    Returns:
        list: A list of dictionaries representing valid actions, with keys 'name', 'cost' and 'profit'.
    """
    stocks = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cost = float(row["Coût par action (en euros)"])
                profit_percent = float(row["Bénéfice (après 2 ans)"].replace("%", ""))
                if cost > 0 and profit_percent > 0:
                    stocks.append({"name": row["Actions #"], "cost": cost, "profit": profit_percent})
            except ValueError:
                continue
    return stocks


def profit_calculation(stocks):
    """
    Calculate the absolute profit (in euros) of each share after 2 years.

    Profit is calculated from the cost and profit percentage provided in the input data,
    and added as a new 'profit_value' key to each dictionary.

    Args:
        stocks (list): List of dictionaries representing stocks, with 'cost' and 'profit' keys.
    """
    for stock in stocks:
        if stock["cost"] > 0 and stock["profit"] > 0:
            stock["profit_value"] = (float(stock["cost"])) * (((float(stock["profit"])))) / 100


def find_best_combination_optimized(stocks):
    """
    Trouve la combinaison d'actions la plus rentable sans dépasser le budget MAX_BUDGET.
    Implémente une version optimisée du problème du sac à dos (0/1 knapsack).
    """

    precision = 100  # Pour gérer les floats en euros avec 2 décimales
    max_capacity = int(MAX_BUDGET * precision)

    # Convertir les coûts en entiers pour les utiliser comme indices
    for stock in stocks:
        stock["cost_int"] = int(stock["cost"] * precision)

    # Initialiser la table de DP
    dp = [0.0] * (max_capacity + 1)
    selected = [[] for _ in range(max_capacity + 1)]

    # Parcours des actions
    for stock in stocks:
        for c in range(max_capacity, stock["cost_int"] - 1, -1):
            new_profit = dp[c - stock["cost_int"]] + stock["profit_value"]
            if new_profit > dp[c]:
                dp[c] = new_profit
                selected[c] = selected[c - stock["cost_int"]] + [stock]

    best_profit = max(dp)
    best_index = dp.index(best_profit)
    best_combination = selected[best_index]

    return best_combination, best_profit


if __name__ == "__main__":
    start = time.time()

    stocks = load_data(file_path)
    profit_calculation(stocks)
    best_combination, best_profit = find_best_combination_optimized(stocks)

    print("Best stock combination:")
    total_cost = 0
    for stock in best_combination:
        print(f"{stock['name']} - Cost: {stock['cost']} € - Profit: {stock['profit_value']:.2f} €")
        total_cost += stock["cost"]

    print(f"\nTotal cost: {total_cost:.2f} €")
    print(f"Total profit: {best_profit:.2f} €")

    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
