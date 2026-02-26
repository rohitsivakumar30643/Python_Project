def calculate_emi(principal, rate, tenure):
    if tenure <= 0:
        raise ValueError("Tenure must be greater than 0.")
    if principal <= 0:
        raise ValueError("Principal must be greater than 0.")

    monthly_rate = rate / (12 * 100)
    if monthly_rate == 0:
        return round(principal / tenure, 2)

    emi = (principal * monthly_rate * pow(1 + monthly_rate, tenure)) / \
          (pow(1 + monthly_rate, tenure) - 1)
    return round(emi, 2)
