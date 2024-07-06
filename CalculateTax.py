class calculateTax(object):
    def __init__(self, earn):
        self.earn = earn
        self.tax_brackets = [
            (0, 14000, 0.105),
            (14000, 48000, 0.175),
            (48000, 70000, 0.30),
            (70000, 180000, 0.33),
            (180000, float('inf'), 0.39)
        ]

    def calculate(self):
        annual_income = self.earn * 52

        # Calculate annual tax
        annual_tax = 0
        for lower, upper, rate in self.tax_brackets:
            if annual_income > lower:
                taxable_income = min(annual_income, upper) - lower
                annual_tax += taxable_income * rate
            else:
                break

        # Calculate weekly tax
        weekly_tax = annual_tax / 52

        # Calculate ACC levy (1.46% of gross earnings)
        acc_levy = self.earn * 0.0146

        # Calculate total weekly deductions
        total_deductions = weekly_tax + acc_levy

        # Calculate net pay
        net_pay = self.earn - total_deductions

        return net_pay
