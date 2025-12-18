"""
3️⃣ Design an Employee Recognition System
❓ Problem Statement

Employees can recognize each other with awards.

Constraints:
    A user cannot award themselves
    Each award has a reason
    System should be easy to extend

🎯 What Achievers is Evaluating
    Business rule enforcement
    Domain modeling
    Readable, expressive code
    Correctness over cleverness
"""


from datetime import datetime
from typing import List


class RecognitionError(Exception):
    pass


class Employee:
    def __init__(self, employee_id: str, name: str) -> None:
        self.employee_id = employee_id
        self.name = name


class Recognition:
    def __init__(
        self,
        from_employee: Employee,
        to_employee: Employee,
        message: str,
        timestamp: datetime,
    ) -> None:
        self.from_employee = from_employee
        self.to_employee = to_employee
        self.message = message
        self.timestamp = timestamp


class RecognitionService:
    def __init__(self) -> None:
        self._recognitions: List[Recognition] = []

    def recognize(
        self,
        from_employee: Employee,
        to_employee: Employee,
        message: str,
    ) -> None:
        if from_employee.employee_id == to_employee.employee_id:
            raise RecognitionError("Employees cannot recognize themselves")

        recognition = Recognition(
            from_employee=from_employee,
            to_employee=to_employee,
            message=message,
            timestamp=datetime.utcnow(),
        )
        self._recognitions.append(recognition)

    def get_recognitions_for_employee(self, employee_id: str) -> List[Recognition]:
        return [
            r for r in self._recognitions
            if r.to_employee.employee_id == employee_id
        ]


# ---- Usage Example ----
alice = Employee("1", "Alice")
bob = Employee("2", "Bob")

service = RecognitionService()
service.recognize(alice, bob, "Great job on the Q4 project!")

recognitions = service.get_recognitions_for_employee("2")
print(len(recognitions))  # 1
