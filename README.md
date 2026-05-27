# Smart Budget Tracker

A personal finance tracking application built with Python and Kivy. Track income and expenses, visualize spending habits, and manage monthly budgets through a clean GUI.

---

## Features

- **Expense & Income Tracking** — Log transactions with amount, category, and date
- **Summary Dashboard** — View total income, expenses, and balance with color-coded status
- **Spending Insights** — Automatically detects your biggest expense, top spending category, monthly trends, and savings rate
- **Budget Manager** — Set monthly limits per category with live warnings at 80% and alerts when exceeded
- **Data Visualization** — Three built-in charts powered by matplotlib:
  - Spending by category (pie chart)
  - Monthly spending trends (bar chart)
  - Income vs expenses comparison (bar chart)
- **Persistent Storage** — All data saved locally to JSON, automatically loaded on startup

---

## Screenshots

![Home Screen](screenshots/home.png)
![Summary](screenshots/summary.png)
![Charts](screenshots/charts.png)

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Kivy | GUI framework |
| matplotlib | Data visualization |
| JSON | Local data persistence |

---

## Project Structure

```
Budget Tracker/
├── main.py          # Kivy app — all screens and navigation
├── utils.py         # Core logic — add, load, save, summarize, budget checks
├── graphs.py        # Chart generation using matplotlib
├── budget.kv        # Kivy layout file — all UI definitions
└── expenses.json    # Auto-generated data file (created on first run)
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/budget-tracker.git
cd budget-tracker
```

### 2. Install dependencies

```bash
pip install kivy matplotlib
```

### 3. Run the app

```bash
python main.py
```

---

## How to Use

1. **Add Expense / Add Income** — Enter an amount, category or source, and date in YYYY-MM-DD format
2. **View Expenses / View Income** — Scrollable list of all recorded transactions
3. **Summary** — Instant overview of your financial balance and category breakdown
4. **Budget Manager** — Set a monthly spending limit for any category; the app warns you as you approach or exceed it
5. **Spending Insights** — Automatic analysis of your habits including biggest purchase, average spend, top category, and savings rate
6. **View Graphs** — Generate charts from your real data with one tap

---

## What I Learned

- Building multi-screen GUI applications with Kivy and KV language
- Separating UI logic from business logic across multiple files
- Persisting and loading structured data using JSON
- Generating and embedding matplotlib charts inside a Kivy app
- Handling real-world Python issues like file path anchoring with `__file__` and image cache invalidation
- Incremental project development across multiple phases

---

## Future Improvements

- Recurring transaction support
- Export data to CSV
- Date range filtering
- Dark/light theme toggle
- Mobile packaging with Buildozer (Android/iOS)
- Better Looking UI
- Financial Ai Support

---

## Author

Built by Tyler Renda.
[GitHub](https://github.com/yourusername) • [LinkedIn](https://www.linkedin.com/in/tyler-renda-85ba3333a/)