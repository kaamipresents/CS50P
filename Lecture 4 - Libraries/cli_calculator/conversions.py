def convert_length(value, from_unit, to_unit):
    length_units = {
        "meter": 1,
        "kilometer": 1000,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254
    }
    if from_unit not in length_units or to_unit not in length_units:
        print("Invalid length units. Please choose from meter, kilometer, centimeter, millimeter, mile, yard, foot, inch.")
        return
    try:
        value = float(value)
        value_in_meters = value * length_units[from_unit]
        converted_value = value_in_meters / length_units[to_unit]
        return f"{value} {from_unit} is equal to {converted_value} {to_unit}."
    except ValueError:
        print("Please provide a valid numeric value for conversion.")
        return

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
        
def convert_temperature(value, from_unit, to_unit):
    temp_units = ["c","f","k"]
    if from_unit not in temp_units or to_unit not in temp_units:
        print("Invalid temperature units. Please choose from C, F, K.")
        return
    try:
        value = float(value)
        if from_unit == "c":
            c = value
        elif from_unit == "f":
            c = (value - 32) * 5/9
        elif from_unit == "k":
            c = value - 273.15
        if to_unit == "c":
            result = c
        elif to_unit == "f":
            result = (c * 9/5) + 32
        elif to_unit == "k":
            result = c + 273.15
        return f"{value} {from_unit} is equal to {result} {to_unit}."
    except ValueError:
        print("Please provide a valid numeric value for conversion.")
        return