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