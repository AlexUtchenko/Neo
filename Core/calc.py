result = None
operand = None
operator = None
wait_for_number = False


while True:

    while not result: # the first operand 
        data = input(">>> ")
        try:
            result = float(data)
            wait_for_number = False
        except ValueError:
            print(f"{data} is not a number, try again")
            continue

    while not wait_for_number: # operator
        data = input(">>> ")
        if not wait_for_number and data in ('+', '-', '*', '/', '='):
            operator = data
            wait_for_number = True
        else:
            print(f"{data} is an unknown operator, try again")
            continue

    if operator == '=':
        print(result)
        break

    while wait_for_number: # operand
        operand = input(">>> ")
        try:
            operand = float(operand)
            wait_for_number = False
        except ValueError:
            print(f"{data} is not a number, try again")
            continue

    # calculations
    if operator == '+':
        result = result + operand
    elif operator == '-':
        result = result - operand
    elif operator == '*':
        result = result * operand
    elif operator == '/':
        try:
            result = result / operand
        except ZeroDivisionError:
            while True:
                operand = input("Enter correct operand value for division operation >>>  ")
                if operand.isnumeric() and operand != 0:
                    result = result / float(operand)
                    break
                print(f"{operand} is a wrong operand")
    else:
        print("Ooops. Unpredictable mistake")
