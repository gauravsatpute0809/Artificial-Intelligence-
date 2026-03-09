import itertools

# -------- User Input --------
first_word = input("Enter first word: ").upper()
second_word = input("Enter second word: ").upper()
result_word = input("Enter result word: ").upper()

unique_letters = list(set(first_word + second_word + result_word))

if len(unique_letters) > 10:
    print("Too many unique letters (max 10 allowed).")
    exit()

digit_list = range(10)

for digit_perm in itertools.permutations(digit_list, len(unique_letters)):
    letter_digit_map = dict(zip(unique_letters, digit_perm))

    # Leading letter should not be zero
    if (letter_digit_map[first_word[0]] == 0 or
        letter_digit_map[second_word[0]] == 0 or
        letter_digit_map[result_word[0]] == 0):
        continue

    number1 = int("".join(str(letter_digit_map[ch]) for ch in first_word))
    number2 = int("".join(str(letter_digit_map[ch]) for ch in second_word))
    result_number = int("".join(str(letter_digit_map[ch]) for ch in result_word))

    if number1 + number2 == result_number:
        print("\nSolution Found:\n")

        print("Letter Values:")
        for letter in sorted(letter_digit_map.keys()):
            print(letter, "=", letter_digit_map[letter])

        print("\nVerification:")
        print(number1, "+", number2, "=", result_number)
        break
else:
    print("No solution found")