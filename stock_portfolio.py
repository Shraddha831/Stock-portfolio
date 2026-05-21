import csv
import os
from datetime import datetime

STOCK_PRICES = {
    "AAPL":  182.50,
    "TSLA":  248.00,
    "GOOGL": 175.30,
    "AMZN":  192.80,
    "MSFT":  415.20,
    "NFLX":  628.00,
    "META":  530.10,
    "NVDA":  950.40,
}

DIVIDER = "-" * 50


def show_available_stocks():
    """Display all stocks in the hardcoded price dictionary."""
    print(f"\n{'Ticker':<10} {'Price (USD)':>12}")
    print(DIVIDER)
    for ticker, price in STOCK_PRICES.items():
        print(f"{ticker:<10} ${price:>11.2f}")
    print()


def get_portfolio():
    """Interactively collect stock names and quantities from the user."""
    portfolio = {}

    print("\nEnter your stock holdings.")
    print("Type 'done' when finished, or 'list' to see available stocks.\n")

    while True:
        ticker = input("  Stock ticker (e.g. AAPL): ").strip().upper()

        if ticker == "DONE":
            break
        if ticker == "LIST":
            show_available_stocks()
            continue
        if not ticker:
            continue
        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' not found. Type 'list' to see available stocks.")
            continue

        qty_str = input(f"  Quantity of {ticker}: ").strip()
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("  ⚠  Please enter a positive whole number.")
            continue

        if ticker in portfolio:
            portfolio[ticker] += qty
        else:
            portfolio[ticker] = qty

        print(f"  ✓  Added {qty} × {ticker} @ ${STOCK_PRICES[ticker]:.2f}")

    return portfolio


def calculate_portfolio(portfolio):
    """Return a list of (ticker, qty, price, value) tuples and the grand total."""
    rows = []
    total = 0.0
    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        value = price * qty
        total += value
        rows.append((ticker, qty, price, value))
    return rows, total


def display_report(rows, total):
    """Print a formatted portfolio summary to the console."""
    print(f"\n{'=' * 50}")
    print("         STOCK PORTFOLIO SUMMARY")
    print(f"{'=' * 50}")
    print(f"{'Ticker':<8} {'Qty':>6} {'Price':>12} {'Value':>14}")
    print(DIVIDER)
    for ticker, qty, price, value in rows:
        print(f"{ticker:<8} {qty:>6} ${price:>11.2f} ${value:>13.2f}")
    print(DIVIDER)
    print(f"{'TOTAL':>28}  ${total:>13.2f}")
    print(f"{'=' * 50}\n")


def save_to_txt(rows, total, filename):
    """Save the portfolio report to a plain-text file."""
    with open(filename, "w") as f:
        f.write("STOCK PORTFOLIO REPORT\n")
        f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{DIVIDER}\n")
        f.write(f"{'Ticker':<8} {'Qty':>6} {'Price':>12} {'Value':>14}\n")
        f.write(f"{DIVIDER}\n")
        for ticker, qty, price, value in rows:
            f.write(f"{ticker:<8} {qty:>6} ${price:>11.2f} ${value:>13.2f}\n")
        f.write(f"{DIVIDER}\n")
        f.write(f"{'TOTAL VALUE':<28}  ${total:>13.2f}\n")
    print(f"  ✓  Report saved → {filename}")


def save_to_csv(rows, total, filename):
    """Save the portfolio data to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Quantity", "Price (USD)", "Value (USD)"])
        for ticker, qty, price, value in rows:
            writer.writerow([ticker, qty, f"{price:.2f}", f"{value:.2f}"])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", f"{total:.2f}"])
    print(f"  ✓  CSV saved → {filename}")


def ask_save(rows, total):
    """Ask the user whether to save the report and in which format."""
    print("Would you like to save the report?")
    print("  1) Save as .txt")
    print("  2) Save as .csv")
    print("  3) Save both")
    print("  4) Skip")
    choice = input("\n  Enter choice (1-4): ").strip()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if choice in ("1", "3"):
        save_to_txt(rows, total, f"portfolio_{stamp}.txt")
    if choice in ("2", "3"):
        save_to_csv(rows, total, f"portfolio_{stamp}.csv")
    if choice == "4":
        print("  Report not saved.")


def main():
    print("=" * 50)
    print("     STOCK PORTFOLIO TRACKER")
    print("=" * 50)
    print(f"  Prices as of today (hardcoded demo data).")
    print(f"  Type 'list' at any prompt to see all stocks.")

    show_available_stocks()

    portfolio = get_portfolio()

    if not portfolio:
        print("\n  No stocks entered. Exiting.")
        return

    rows, total = calculate_portfolio(portfolio)
    display_report(rows, total)
    ask_save(rows, total)

    print("\n  Thanks for using Stock Portfolio Tracker!\n")


if __name__ == "__main__":
    main()
