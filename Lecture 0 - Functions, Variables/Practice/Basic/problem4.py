# Invoice ID Formatter

# ask user their invoice number
invoice_number = int(input("Please enter your invoice number: "))

# print the invoice number with 000 added
print(f"Your invoice number is: {invoice_number:05d}")
