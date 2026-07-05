import csv

from database import add_medicine

with open("medicines.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        add_medicine(
            row["brand_name"],
            row["generic_name"],
            row["uses"],
            row["dosage"],
            row["side_effects"],
            row["warnings"]
        )

print("All medicines added successfully.")