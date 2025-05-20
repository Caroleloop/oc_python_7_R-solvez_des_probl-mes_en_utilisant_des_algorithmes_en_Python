import csv
from itertools import combinations
import time


# File path
file_path = "C:/Formation/Projet_07/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

# Maximum budget
MAX_BUDGET = 500


def load_file(filename):
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


def find_best_combination(stocks):
    """
    Find the most profitable combination of actions without exceeding the maximum budget.

    Uses a brute-force approach to test all possible combinations of actions,
    and selects the one that maximizes total profit without exceeding MAX_BUDGET.

    Args:
        stocks (list): List of dictionaries representing stocks, with the keys 'cost' and 'profit_value'.

    Returns:
        tuple: A pair (best_combination, best_total_profit), where
            - best_combination is a list of selected actions,
            - best_total_profit is the corresponding total profit.
    """
    best_profit = 0
    best_combination = []
    for i in range(1, len(stocks) + 1):
        for combo in combinations(stocks, i):
            total_cost = sum(a["cost"] for a in combo)
            if total_cost <= MAX_BUDGET:
                total_profit = sum(a["profit_value"] for a in combo)
                if total_profit > best_profit:
                    best_profit = total_profit
                    best_combination = combo
    return best_combination, best_profit


if __name__ == "__main__":
    start = time.time()

    stocks = load_file(file_path)
    profit_calculation(stocks)
    best_combination, best_profit = find_best_combination(stocks)
    print("Best stock combination:")
    for stock in best_combination:
        print(f"{stock['name']} - Cost: {stock['cost']} € - Profit: {stock['profit_value']:.2f} €")
    print(f"\nTotal profit: {best_profit:.2f} €")

    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
