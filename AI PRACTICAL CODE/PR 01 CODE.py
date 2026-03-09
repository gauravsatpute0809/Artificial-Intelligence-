def create_magic_square(size):
    
    # Magic square works only for odd numbers
    if size % 2 == 0:
        print("Magic Square works only for odd numbers!")
        return

    # Create empty matrix
    square = [[0 for _ in range(size)] for _ in range(size)]

    # Starting position
    row = size // 2
    col = size - 1

    current_number = 1

    while current_number <= size * size:

        # Special condition
        if row == -1 and col == size:
            row = 0
            col = size - 2
        else:
            # Wrap column
            if col == size:
                col = 0

            # Wrap row
            if row < 0:
                row = size - 1

        # If cell already filled
        if square[row][col] != 0:
            col -= 2
            row += 1
            continue
        else:
            square[row][col] = current_number
            current_number += 1

        # Move to next position
        col += 1
        row -= 1

    # Print Magic Square
    print("\nMagic Square for n =", size)
    print("Sum of each row/column =", size * (size * size + 1) // 2)
    print()

    for r in square:
        for value in r:
            print(f"{value:2d}", end=" ")
        print()


# Driver Code
number = int(input("Enter the Number (ODD) of rows of the Magic Square: "))
create_magic_square(number)