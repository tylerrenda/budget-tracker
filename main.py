import os
import io
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.cache import Cache
from utils import load_data, save_data, add_expense, add_income, show_summary, spending_insights
from graphs import pie_chart, bar_chart_monthly, bar_chart_income_vs_expenses

Builder.load_file("budget.kv")


class HomeScreen(Screen):
    pass


class AddExpenseScreen(Screen):
    status_msg = StringProperty("")

    def submit_expense(self):
        app = App.get_running_app()

        amount_text = self.ids.amount_input.text.strip()
        category = self.ids.category_input.text.strip().title()
        date = self.ids.date_input.text.strip()

        try:
            amount = float(amount_text)
            if amount <= 0:
                self.status_msg = "Amount must be a positive number."
                return
        except ValueError:
            self.status_msg = "Invalid amount — numbers only."
            return

        if not category:
            self.status_msg = "Please enter a category."
            return

        if len(date) != 10 or date[4] != "-" or date[7] != "-":
            self.status_msg = "Date must be YYYY-MM-DD (e.g. 2026-06-01)"
            return

        app.expenses = add_expense(app.expenses, amount, category, date)
        save_data(app.expenses, app.income_list, app.budgets)

        self.ids.amount_input.text = ""
        self.ids.category_input.text = ""
        self.ids.date_input.text = ""
        self.status_msg = f"Saved! ${amount:.2f} on {category}"


class ViewExpensesScreen(Screen):
    def on_enter(self):
        self.load_expenses()

    def load_expenses(self):
        app = App.get_running_app()
        container = self.ids.expenses_container
        container.clear_widgets()

        if not app.expenses:
            container.add_widget(Label(
                text="No expenses yet.",
                font_size="16sp",
                size_hint_y=None,
                height=40,
                color=(0.7, 0.7, 0.7, 1)
            ))
            return

        for e in reversed(app.expenses):
            row = Label(
                text=f"{e['date']}   {e['category']}   ${e['amount']:.2f}",
                font_size="15sp",
                size_hint_y=None,
                height=40,
                color=(1, 1, 1, 1)
            )
            container.add_widget(row)


class AddIncomeScreen(Screen):
    status_msg = StringProperty("")

    def submit_income(self):
        app = App.get_running_app()

        amount_text = self.ids.amount_input.text.strip()
        source = self.ids.source_input.text.strip().title()
        date = self.ids.date_input.text.strip()

        try:
            amount = float(amount_text)
            if amount <= 0:
                self.status_msg = "Amount must be a positive number."
                return
        except ValueError:
            self.status_msg = "Invalid amount — numbers only."
            return

        if not source:
            self.status_msg = "Please enter a source."
            return

        if len(date) != 10 or date[4] != "-" or date[7] != "-":
            self.status_msg = "Date must be YYYY-MM-DD (e.g. 2026-06-01)"
            return

        app.income_list = add_income(app.income_list, amount, source, date)
        save_data(app.expenses, app.income_list, app.budgets)

        self.ids.amount_input.text = ""
        self.ids.source_input.text = ""
        self.ids.date_input.text = ""
        self.status_msg = f"Saved! ${amount:.2f} from {source}"


class ViewIncomeScreen(Screen):
    def on_enter(self):
        self.load_income()

    def load_income(self):
        app = App.get_running_app()
        container = self.ids.income_container
        container.clear_widgets()

        if not app.income_list:
            container.add_widget(Label(
                text="No income yet.",
                font_size="16sp",
                size_hint_y=None,
                height=40,
                color=(0.7, 0.7, 0.7, 1)
            ))
            return

        for i in reversed(app.income_list):
            row = Label(
                text=f"{i['date']}   {i['source']}   ${i['amount']:.2f}",
                font_size="15sp",
                size_hint_y=None,
                height=40,
                color=(1, 1, 1, 1)
            )
            container.add_widget(row)


class SummaryScreen(Screen):
    income_text = StringProperty("Total Income:     $0.00")
    expenses_text = StringProperty("Total Expenses:  $0.00")
    balance_text = StringProperty("Balance:             $0.00")
    status_text = StringProperty("")
    balance_color = ListProperty([1, 1, 1, 1])
    status_color = ListProperty([1, 1, 1, 1])

    def on_enter(self):
        self.load_summary()

    def load_summary(self):
        app = App.get_running_app()
        expenses = app.expenses
        income_list = app.income_list

        total_expenses = sum(e["amount"] for e in expenses)
        total_income = sum(i["amount"] for i in income_list)
        balance = total_income - total_expenses

        self.income_text = f"Total Income:     ${total_income:.2f}"
        self.expenses_text = f"Total Expenses:  ${total_expenses:.2f}"
        self.balance_text = f"Balance:             ${balance:.2f}"

        if balance < 0:
            self.balance_color = [1, 0.3, 0.3, 1]
            self.status_text = "You are spending more than you earn!"
            self.status_color = [1, 0.3, 0.3, 1]
        elif balance == 0:
            self.balance_color = [1, 0.8, 0.2, 1]
            self.status_text = "Breaking even — try to save a little!"
            self.status_color = [1, 0.8, 0.2, 1]
        else:
            self.balance_color = [0.2, 0.9, 0.4, 1]
            self.status_text = "You are in the green!"
            self.status_color = [0.2, 0.9, 0.4, 1]

        container = self.ids.category_container
        container.clear_widgets()

        if expenses:
            categories = {}
            for e in expenses:
                cat = e["category"]
                categories[cat] = categories.get(cat, 0) + e["amount"]

            for cat, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                container.add_widget(Label(
                    text=f"{cat}:  ${total:.2f}",
                    font_size="15sp",
                    size_hint_y=None,
                    height=35,
                    color=(1, 1, 1, 1)
                ))


class InsightsScreen(Screen):
    def on_enter(self):
        self.load_insights()

    def load_insights(self):
        app = App.get_running_app()
        expenses = app.expenses
        income_list = app.income_list
        container = self.ids.insights_container
        container.clear_widgets()

        def add_line(text, color=(1, 1, 1, 1)):
            container.add_widget(Label(
                text=text,
                font_size="15sp",
                size_hint_y=None,
                height=40,
                color=color,
                halign="left",
                text_size=(container.width, None)
            ))

        if not expenses:
            add_line("No expenses to analyze yet.", color=(0.7, 0.7, 0.7, 1))
            return

        biggest = max(expenses, key=lambda e: e["amount"])
        add_line(
            f"Biggest expense: ${biggest['amount']:.2f} on {biggest['category']} ({biggest['date']})",
            color=(1, 0.6, 0.2, 1)
        )

        avg = sum(e["amount"] for e in expenses) / len(expenses)
        add_line(f"Average expense: ${avg:.2f}", color=(0.8, 0.8, 1, 1))

        categories = {}
        for e in expenses:
            cat = e["category"]
            categories[cat] = categories.get(cat, 0) + e["amount"]

        top_category = max(categories, key=categories.get)
        total_spent = sum(categories.values())
        top_percent = (categories[top_category] / total_spent) * 100
        add_line(
            f"Top category: {top_category} (${categories[top_category]:.2f} — {top_percent:.1f}%)",
            color=(0.4, 0.9, 1, 1)
        )

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
            add_line(
                f"Spending is {direction} ${abs(diff):.2f} vs last month",
                color=(1, 0.4, 0.4, 1) if diff > 0 else (0.2, 0.9, 0.4, 1)
            )

        total_income = sum(i["amount"] for i in income_list)
        if total_income > 0:
            savings_rate = ((total_income - total_spent) / total_income) * 100
            color = (0.2, 0.9, 0.4, 1) if savings_rate > 0 else (1, 0.3, 0.3, 1)
            label = (
                f"Savings rate: {savings_rate:.1f}% of income saved"
                if savings_rate > 0
                else f"Overspending by {abs(savings_rate):.1f}% of income"
            )
            add_line(label, color=color)


class BudgetScreen(Screen):
    status_msg = StringProperty("")

    def on_enter(self):
        self.load_budgets()

    def load_budgets(self):
        app = App.get_running_app()
        container = self.ids.budget_container
        container.clear_widgets()

        if not app.budgets:
            container.add_widget(Label(
                text="No budgets set yet.",
                font_size="16sp",
                size_hint_y=None,
                height=40,
                color=(0.7, 0.7, 0.7, 1)
            ))
            return

        categories = {}
        for e in app.expenses:
            cat = e["category"]
            categories[cat] = categories.get(cat, 0) + e["amount"]

        for category, limit in app.budgets.items():
            spent = categories.get(category, 0)
            remaining = limit - spent
            percent = (spent / limit) * 100 if limit > 0 else 0

            if spent > limit:
                color = (1, 0.3, 0.3, 1)
                status = f"OVER BUDGET by ${abs(remaining):.2f}!"
            elif percent >= 80:
                color = (1, 0.8, 0.2, 1)
                status = f"Warning — only ${remaining:.2f} left"
            else:
                color = (0.2, 0.9, 0.4, 1)
                status = f"${remaining:.2f} remaining"

            container.add_widget(Label(
                text=f"{category}  |  Budget: ${limit:.2f}  |  Spent: ${spent:.2f}  |  {status}",
                font_size="14sp",
                size_hint_y=None,
                height=44,
                color=color,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None)
            ))

    def submit_budget(self):
        app = App.get_running_app()

        category = self.ids.category_input.text.strip().title()
        limit_text = self.ids.limit_input.text.strip()

        if not category:
            self.status_msg = "Please enter a category name."
            return

        try:
            limit = float(limit_text)
            if limit <= 0:
                self.status_msg = "Limit must be a positive number."
                return
        except ValueError:
            self.status_msg = "Invalid amount — numbers only."
            return

        app.budgets[category] = limit
        save_data(app.expenses, app.income_list, app.budgets)

        self.ids.category_input.text = ""
        self.ids.limit_input.text = ""
        self.status_msg = f"Budget set — {category}: ${limit:.2f}"
        self.load_budgets()

    def delete_budget(self):
        app = App.get_running_app()
        category = self.ids.category_input.text.strip().title()

        if not category:
            self.status_msg = "Enter a category name to delete."
            return

        if category not in app.budgets:
            self.status_msg = f"{category} has no budget set."
            return

        del app.budgets[category]
        save_data(app.expenses, app.income_list, app.budgets)

        self.ids.category_input.text = ""
        self.ids.limit_input.text = ""
        self.status_msg = f"Budget for {category} removed."
        self.load_budgets()


class GraphsScreen(Screen):
    def show_pie_chart(self):
        app = App.get_running_app()
        if not app.expenses:
            self.ids.graphs_status.text = "No expenses to graph yet."
            return
        path = pie_chart(app.expenses)
        self.display_chart(path)

    def show_bar_monthly(self):
        app = App.get_running_app()
        if not app.expenses:
            self.ids.graphs_status.text = "No expenses to graph yet."
            return
        path = bar_chart_monthly(app.expenses)
        self.display_chart(path)

    def show_income_vs_expenses(self):
        app = App.get_running_app()
        if not app.expenses and not app.income_list:
            self.ids.graphs_status.text = "No data to graph yet."
            return
        path = bar_chart_income_vs_expenses(app.expenses, app.income_list)
        self.display_chart(path)

    def display_chart(self, path):
        if not path:
            self.ids.graphs_status.text = "Could not generate chart."
            return

        Cache.remove("kv.image", path)
        Cache.remove("kv.texture", path)

        container = self.ids.chart_container
        container.clear_widgets()
        img = KivyImage(
            source=path,
            allow_stretch=True,
            keep_ratio=True
        )
        container.add_widget(img)
        self.ids.graphs_status.text = ""

class BudgetScreenManager(ScreenManager):
    pass

class BudgetApp(App):
    def build(self):
        self.expenses, self.income_list, self.budgets = load_data()
        return BudgetScreenManager()

if __name__ == "__main__":
    BudgetApp().run()