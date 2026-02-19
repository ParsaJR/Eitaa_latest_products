def interactive_phone_number() -> list[int]:

    phone_numbers: list[int] = []

    print(
        "Please enter the phoneNumber(s) that you are willing to log-in with. (E.g. 09123456789) \n Empty line breaks the loop:"
    )
    while True:
        num = input()
        if not num:
            if len(phone_numbers) < 1:
                quit()
            break
        if len(num) < 10:
            print("Please enter a valid phone number")
            continue

        # Eitaa's login page does not need the first zero. It will automatically
        # prefix the number with the iranian country-calling-code.
        num = num.lstrip("0")

        phone_numbers.append(int(num))

    return phone_numbers
