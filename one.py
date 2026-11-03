#name = Satyam kumar
#email = satyam.kumar8@rungta.org
#ERP = RU-26-02546
#section = B2
#ps no. = 5


"""E-Commerce Sales Analyzer - Project 5."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

COLUMNS = ["Order_ID", "Product", "Category", "Quantity", "Price"]

def load_orders(filename):
    """Read orders from a CSV, validate each row, and return valid orders and skipped-row reasons."""
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [c for c in COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError("Missing CSV columns: " + ", ".join(missing))
    valid, skipped = [], []
    for row_no, row in enumerate(raw.to_dict(orient="records"), start=1):
        oid, product, category = (row[c].strip() for c in COLUMNS[:3])
        qtext, ptext = row["Quantity"].strip(), row["Price"].strip()
        if not oid or not product or not category:
            skipped.append((row_no, "Order_ID, Product and Category cannot be empty")); continue
        try:
            quantity = int(qtext)
        except ValueError:
            skipped.append((row_no, f"invalid Quantity '{qtext}'")); continue
        try:
            price = float(ptext)
        except ValueError:
            skipped.append((row_no, f"invalid Price '{ptext}'")); continue
        # Price is checked first to match the assignment's negative-price example.
        if price <= 0:
            skipped.append((row_no, "Price must be positive")); continue
        if quantity <= 0:
            skipped.append((row_no, "Quantity must be positive")); continue
        valid.append({"Order_ID": oid, "Product": product, "Category": category,
                      "Quantity": quantity, "Price": price, "Revenue": quantity * price})
    return pd.DataFrame(valid, columns=COLUMNS + ["Revenue"]), skipped

def analyze(orders):
    """Calculate overall sales totals and revenue rankings for products and categories."""
    if orders.empty:
        raise ValueError("No valid order records were found.")
    products = (orders.groupby("Product", as_index=False)
                .agg(Units_Sold=("Quantity", "sum"), Revenue=("Revenue", "sum"))
                .sort_values(["Revenue", "Product"], ascending=[False, True]))
    categories = (orders.groupby("Category", as_index=False)["Revenue"].sum()
                  .sort_values("Revenue", ascending=False))
    total = float(orders["Revenue"].sum())
    categories["Percentage"] = categories["Revenue"] / total * 100
    top = products.iloc[0]
    return {"total": total, "orders": len(orders),
            "units": int(orders["Quantity"].sum()),
            "products": products, "categories": categories,
            "top_name": top["Product"], "top_revenue": float(top["Revenue"])}

def summary(orders, skipped):
    """Print the sales summary and skipped-row details, then return the analysis results."""
    r = analyze(orders)
    print("\n========== SALES SUMMARY ==========")
    print(f"Total Revenue: {r['total']:.0f}")
    print(f"Orders: {r['orders']}")
    print(f"Units sold: {r['units']}")
    print(f"Top product:{r['top_name']}({r['top_revenue']:.0f})")
    if skipped:
        for row, reason in skipped:
            print(f"Row {row} skipped: {reason}")
    else:
        print("Skipped rows: 0")
    print("\nTop 5 selling products by revenue:")
    print(r["products"].head(5).to_string(index=False))
    return r

def category_report(r):
    """Print each category's revenue and its percentage of total revenue."""
    print("\n========== CATEGORY-WISE REVENUE ==========")
    for row in r["categories"].itertuples(index=False):
        print(f"{row.Category}:{row.Revenue:.0f}({row.Percentage:.2f}%)")

def make_charts(r, folder="."):
    """Save product-revenue and category-revenue charts in the target folder and return their paths."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    top = r["products"].head(5)
    plt.figure(figsize=(9, 5))
    bars = plt.bar(top["Product"], top["Revenue"])
    plt.title("Top 5 Selling Products by Revenue")
    plt.xlabel("Product"); plt.ylabel("Revenue"); plt.grid(axis="y", alpha=.25)
    for bar, value in zip(bars, top["Revenue"]):
        plt.text(bar.get_x()+bar.get_width()/2, bar.get_height(), f"{value:.0f}",
                 ha="center", va="bottom")
    plt.tight_layout()
    barfile = folder / "top_products.png"
    plt.savefig(barfile, dpi=150); plt.close()
    cats = r["categories"]
    plt.figure(figsize=(7, 7))
    plt.pie(cats["Revenue"], labels=cats["Category"], autopct="%1.2f%%", startangle=90)
    plt.title("Category-wise Revenue")
    plt.tight_layout()
    piefile = folder / "category_revenue.png"
    plt.savefig(piefile, dpi=150); plt.close()
    return barfile, piefile

def main():
    """Parse the CSV argument, load orders, run the interactive report menu, and return an exit code."""
    parser = argparse.ArgumentParser(description="Analyze e-commerce orders from CSV.")
    parser.add_argument("csv_file", nargs="?", default="orders.csv")
    args = parser.parse_args()
    try:
        orders, skipped = load_orders(args.csv_file)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        print(f"Error: {exc}"); return 1
    if orders.empty:
        print("No valid orders to analyze.")
        for row, reason in skipped: print(f"Row {row} skipped: {reason}")
        return 1
    while True:
        print("\n===== E-Commerce Sales Analyzer =====")
        print("1. Sales Summary\n2. Category-wise Revenue\n3. Generate Charts\n4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            summary(orders, skipped)
        elif choice == "2":
            category_report(analyze(orders))
        elif choice == "3":
            files = make_charts(analyze(orders))
            print(f"Charts saved: {files[0]} and {files[1]}")
        elif choice == "4":
            print("Thank you for using E-Commerce Sales Analyzer."); break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
