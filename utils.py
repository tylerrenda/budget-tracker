import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses.json")

def add_income(income_list, amount, source, date):
    income = {
        "amount": amount,
        "source": source,
        "date": date
    }
    income_list.append(income)
    return income_list

def view_income(income_list):
    if not income_list:
        print("\nNo income recorded yet.")
        return
    print("\n--- Your Income ---")
    for i, inc in enumerate(income_list, 1):
        print(f"{i}. {inc['date']} | {inc['source']} | ${inc['amount']:.2f}")
    print("-------------------")

def show_summary(expenses, income_list):
    total_expenses = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income_list)
    balance = total_income - total_expenses

    print("\n====== Summary ======")
    print(f"Total Income:   ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Balance:        ${balance:.2f}")

    if balance < 0:
        print(" You're spending more than you're earning!")
    elif balance == 0:
        print("Breaking even — try to save a little!")
    else:
        print("You're in the green!")

    # Category breakdown
    if expenses:
        print("\n--- Spending by Category ---")
        categories = {}
        for e in expenses:
            cat = e["category"]
            categories[cat] = categories.get(cat, 0) + e["amount"]
        for cat, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: ${total:.2f}")
    print("=====================")

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("expenses", []), data.get("income", []), data.get("budgets", {})
    except FileNotFoundError:
        return [], [], {}
    
def save_data(expenses, income_list, budgets):
    data = {
        "expenses": expenses,
        "income": income_list,
        "budgets": budgets
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense(expenses, amount, category, date):
    expense = {
        "amount": amount,
        "category": category,
        "date": date
    }
    expenses.append(expense)
    return expenses

def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\n--- Your Expenses ---")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['category']} | ${e['amount']:.2f}")
    print("---------------------")

def load_budgets():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("budgets", {})
    except FileNotFoundError:
        return {}

def save_budgets(expenses, income_list, budgets):
    data = {
        "expenses": expenses,
        "income": income_list,
        "budgets": budgets
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def set_budget(budgets, category, limit):
    budgets[category.title()] = limit
    return budgets

def check_budgets(expenses, budgets):
    if not budgets:
        print("\nNo budgets set yet.")
        return

    # Add up spending per category
    categories = {}
    for e in expenses:
        cat = e["category"]
        categories[cat] = categories.get(cat, 0) + e["amount"]

    print("\n====== Budget Status ======")
    for category, limit in budgets.items():
        spent = categories.get(category, 0)
        remaining = limit - spent
        percent = (spent / limit) * 100 if limit > 0 else 0

        print(f"\n{category}:")
        print(f"  Budget:  ${limit:.2f}")
        print(f"  Spent:   ${spent:.2f}  ({percent:.1f}%)")

        if spent > limit:
            print(f"  ❌ OVER BUDGET by ${abs(remaining):.2f}!")
        elif percent >= 80:
            print(f"  ⚠️  Warning: Only ${remaining:.2f} left!")
        else:
            print(f"  ✅ Remaining: ${remaining:.2f}")
    print("===========================")

def spending_insights(expenses, income_list):
    if not expenses:
        print("\nNo expenses to analyze yet.")
        return

    print("\n====== Spending Insights ======")

    # Most expensive single purchase
    biggest = max(expenses, key=lambda e: e["amount"])
    print(f"\n💸 Biggest expense: ${biggest['amount']:.2f} on {biggest['category']} ({biggest['date']})")

    # Average expense
    avg = sum(e["amount"] for e in expenses) / len(expenses)
    print(f"📊 Average expense: ${avg:.2f}")

    # Category totals
    categories = {}
    for e in expenses:
        cat = e["category"]
        categories[cat] = categories.get(cat, 0) + e["amount"]

    top_category = max(categories, key=categories.get)
    total_spent = sum(categories.values())
    top_percent = (categories[top_category] / total_spent) * 100

    print(f"🏆 Top spending category: {top_category} (${categories[top_category]:.2f} — {top_percent:.1f}% of total)")

    # Monthly trend
    monthly = {}
    for e in expenses:
        month = e["date"][:7]
        monthly[month] = monthly.get(month, 0) + e["amount"]

    if len(monthly) >= 2:
        sorted_months = sorted(monthly.keys())
        last = monthly[sorted_months[-1]]
        prev = monthly[sorted_months[-2]]
        diff = last - prev
        direction = "up" if diff > 0 else "down"
        emoji = "📈" if diff > 0 else "📉"
        print(f"{emoji}  Spending is {direction} ${abs(diff):.2f} compared to last month")

    # Savings rate
    total_income = sum(i["amount"] for i in income_list)
    if total_income > 0:
        savings_rate = ((total_income - total_spent) / total_income) * 100
        if savings_rate > 0:
            print(f"💰 Savings rate: {savings_rate:.1f}% of income saved")
        else:
            print(f"⚠️  You're spending {abs(savings_rate):.1f}% more than you earn!")

    print("================================")