"""
2️⃣ Design a Rewards / Points Engine
❓ Problem Statement

Users earn points for actions and can redeem them later.

Requirements:
    Add points
    Redeem points
    Prevent overdraft
    Simple, correct behavior

🎯 What Achievers is Evaluating
    State management
    Validation logic
    Clear domain modeling
    Avoiding over-complexity
"""


class InsufficientPointsError(Exception):
    pass


class UserAccount:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self._points = 0

    def add_points(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Points to add must be positive")
        self._points += amount

    def redeem_points(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Points to redeem must be positive")
        if amount > self._points:
            raise InsufficientPointsError(
                f"User {self.user_id} has insufficient points"
            )
        self._points -= amount

    def get_balance(self) -> int:
        return self._points


class RewardsEngine:
    def __init__(self) -> None:
        self._accounts = {}

    def get_or_create_account(self, user_id: str) -> UserAccount:
        if user_id not in self._accounts:
            self._accounts[user_id] = UserAccount(user_id)
        return self._accounts[user_id]

    def add_points(self, user_id: str, points: int) -> None:
        account = self.get_or_create_account(user_id)
        account.add_points(points)

    def redeem_points(self, user_id: str, points: int) -> None:
        account = self.get_or_create_account(user_id)
        account.redeem_points(points)

    def get_balance(self, user_id: str) -> int:
        account = self.get_or_create_account(user_id)
        return account.get_balance()


# ---- Usage Example ----
engine = RewardsEngine()
engine.add_points("user-1", 100)
engine.redeem_points("user-1", 40)

print(engine.get_balance("user-1"))  # 60
