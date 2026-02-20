def convert_weight(value, from_unit, to_unit):
    weight_units = {
        "kg": 1,
        "lb": 0.45,
        "oz": 35.274
    }
    if from_unit not in weight_units or to_unit not in weight_units:
        print("Invalid weight units. Please choose from kg, lg, oz.")
        return
    try:
        value = float(value)
        value_in_kg = value * weight_units[from_unit]
        converted_value = value_in_kg / weight_units[to_unit]
        return f"{value} {from_unit} is equal to {converted_value} {to_unit}."
    except ValueError:
        print("Please provide a valid numeric value for conversion.")
        return