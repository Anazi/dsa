"""
Problem Statement:
Given an array prices where prices[i] is the price of a stock on day i,
find the maximum profit you can achieve from a single buy and a single sell.

Note: You must buy before you sell.

# Example Usage
prices = [7, 1, 5, 3, 6, 4]
calculator = StockProfitCalculator(prices)
print("Solution:", calculator.brute_force())  # Output: 5

| Day | Price | Min so far | Profit Today | Max Profit |
                           | price - min so far |
| --- | ----- | ---------- | ------------ | ---------- |
| 0   | 7     | 7          | 0            | 0          |
| 1   | 1     | **1**      | 0            | 0          |
| 2   | 5     | 1          | 4            | 4          |
| 3   | 3     | 1          | 2            | 4          |
| 4   | 6     | 1          | **5**        | **5**      |
| 5   | 4     | 1          | 3            | 5          |


================ Explanation ==================
You are given:
A list of stock prices.
prices[i] means:
→ On day i, the stock price is prices[i].
---
Objective:
Find the maximum profit you can achieve —
By:
Buying stock on any day x
Selling stock on a later day y (where y > x)
---
Constraint:
You can't sell before you buy.
(You can only buy once and sell once.)
"""


class BestTimeToBuyStock:
    def __init__(self, stock_prices):
        self.stock_prices = stock_prices

    def get_brute_bad(self):
        # TODO: Don't complicate your brute because then optimal solution gets complicated and WOULDN'T WORK FOR ALL USE-CASES
        buy_idx = 0
        sell_idx = 0

        for idx, price in enumerate(self.stock_prices):
            if (self.stock_prices[buy_idx] > price) and (idx != len(self.stock_prices) - 1):
                buy_idx = idx
                sell_idx = buy_idx

        for s_idx in range(buy_idx + 1, len(self.stock_prices)):
            s_price = self.stock_prices[s_idx]
            if s_price > self.stock_prices[sell_idx]:
                sell_idx = s_idx
        return self.stock_prices[sell_idx] - self.stock_prices[buy_idx]

    def get_brute(self):
        max_profit = 0
        for i in range(len(self.stock_prices)):
            for j in range(i + 1, len(self.stock_prices)):
                profit = self.stock_prices[j] - self.stock_prices[i]
                max_profit = max(max_profit, profit)
        return max_profit

    def get_optimized(self) -> int:
        min_price_so_far = float('inf')  # Start with very high min price
        max_profit = 0  # Start with zero profit

        # Iterate over all days
        for price in self.stock_prices:
            # Thought process:
            # If I had bought at min_price_so_far, what profit today?
            current_profit = price - min_price_so_far
            # Update max_profit if better
            max_profit = max(max_profit, current_profit)
            # Update min_price_so_far if today is cheaper
            min_price_so_far = min(min_price_so_far, price)
        return max_profit


t_prices = [7, 1, 5, 3, 6, 4]
t_prices1 = [10, 2, 8, 1, 3, 4]  # Bad BRUTE solution does not work for this use-case
solver = BestTimeToBuyStock(stock_prices=t_prices1)
print(f'BAD Brute BestTimeToBuyStock: {solver.get_brute_bad()}')
print(f'Brute BestTimeToBuyStock: {solver.get_brute()}')
print(f"Optimized BestTimeToBuyStock: {solver.get_optimized()}")
