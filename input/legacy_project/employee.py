class Employee:

    def __init__(self, name, salary, department):
        self.name = name
        self.salary = salary
        self.department = department

    def calculate_bonus(self):
        if self.salary > 50000:
            return self.salary * 0.10

        return self.salary * 0.05

    def display_info(self):
        return (
            f"{self.name} works in "
            f"{self.department} department"
        )