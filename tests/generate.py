def uposatha_lengths():
    lengths = []
    for number in range(1, 9):
        if number == 3 or number == 7:
            lengths.append(14)
        else:
            lengths.append(15)

    return lengths