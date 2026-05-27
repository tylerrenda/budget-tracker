import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def pie_chart(expenses):
    if not expenses:
        return None

    categories = defaultdict(float)
    for e in expenses:
        categories[e["category"]] += e["amount"]

    labels = list(categories.keys())
    values = list(categories.values())

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Spending by Category")
    plt.tight_layout()

    path = os.path.join(BASE_DIR, "chart_pie.png")
    plt.savefig(path)
    plt.close()
    return path

def bar_chart_monthly(expenses):
    if not expenses:
        return None

    monthly = defaultdict(float)
    for e in expenses:
        month = e["date"][:7]
        monthly[month] += e["amount"]

    sorted_months = sorted(monthly.keys())
    values = [monthly[m] for m in sorted_months]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(sorted_months, values, color="steelblue", edgecolor="black")
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Total Spent ($)")
    plt.xticks(rotation=45)

    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"${val:.2f}",
            ha="center", va="bottom", fontsize=9
        )

    plt.tight_layout()

    path = os.path.join(BASE_DIR, "chart_monthly.png")
    plt.savefig(path)
    plt.close()
    return path

def bar_chart_income_vs_expenses(expenses, income_list):
    total_expenses = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income_list)

    if total_expenses == 0 and total_income == 0:
        return None

    labels = ["Income", "Expenses"]
    values = [total_income, total_expenses]
    colors = ["green", "tomato"]

    plt.figure(figsize=(6, 5))
    bars = plt.bar(labels, values, color=colors, edgecolor="black", width=0.4)
    plt.title("Income vs Expenses")
    plt.ylabel("Amount ($)")

    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"${val:.2f}",
            ha="center", va="bottom", fontsize=10
        )

    plt.tight_layout()

    path = os.path.join(BASE_DIR, "chart_income_vs_expenses.png")
    plt.savefig(path)
    plt.close()
    return path