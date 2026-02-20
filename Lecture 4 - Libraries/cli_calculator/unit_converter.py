# CLI Unit Converter

# libraries import
from sys import argv
from conversions import convert_length, convert_weight, convert_temperature
# python unit_converter.py <unit_type> <value> <from_unit> <to_unit>

def main():
    if len(argv) != 5:
        print("Usage: Arguments required are not provided")
        return
    unit_type = argv[1].lower()
    if unit_type not in ["length", "weight", "temperature"]:
        print("Invalid unit type. Please choose from length, weight, temperature.")
        return
    match unit_type:
        case "length":
            result = convert_length(argv[2], argv[3].lower(), argv[4].lower())
            print(result)
        case "weight":
            result = convert_weight(argv[2], argv[3].lower(), argv[4].lower())  
            print(result)          
        case "temperature":
            result = convert_temperature(argv[2], argv[3].lower(), argv[4].lower())
            print(result)
        case _:
            print("Mentioned Unit Type is conversion is not available")


if __name__ == "__main__":
    main()