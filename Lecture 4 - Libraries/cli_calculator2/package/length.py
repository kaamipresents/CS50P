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