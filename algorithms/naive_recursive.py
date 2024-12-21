def recursive_alignment(x, y, match_score=1, mismatch_penalty=-1, gap_penalty=0):
    """
    Recursive sequence alignment algorithm.

    x, y -- Sequences to align.
    match_score -- Score for matching characters.
    mismatch_penalty -- Penalty for mismatching characters.
    gap_penalty -- Penalty for introducing a gap.
    """
    def align(i, j):
        # Base cases
        if i == 0 and j == 0:
            return 0, []

        if i == 0:
            alignment = []
            for k in range(j):
                alignment.append(("-", y[k]))
            return j * gap_penalty, alignment

        if j == 0:
            alignment = []
            for k in range(i):
                alignment.append((x[k], "-"))
            return i * gap_penalty, alignment

        # Recursive cases
        # Match/mismatch
        match = align(i - 1, j - 1)
        match_score_value = match[0] + (match_score if x[i - 1] == y[j - 1] else mismatch_penalty)
        match_alignment = match[1] + [(x[i - 1], y[j - 1])]

        # Gap in x
        gap_x = align(i, j - 1)
        gap_x_score = gap_x[0] + gap_penalty
        gap_x_alignment = gap_x[1] + [("-", y[j - 1])]

        # Gap in y
        gap_y = align(i - 1, j)
        gap_y_score = gap_y[0] + gap_penalty
        gap_y_alignment = gap_y[1] + [(x[i - 1], "-")]

        # Choose the best option
        if match_score_value >= gap_x_score and match_score_value >= gap_y_score:
            return match_score_value, match_alignment
        elif gap_x_score >= match_score_value and gap_x_score >= gap_y_score:
            return gap_x_score, gap_x_alignment
        else:
            return gap_y_score, gap_y_alignment

    # Start recursion from the lengths of x and y
    score, alignment = align(len(x), len(y))
    return alignment, score


def print_alignment(x, y, alignment):
    """
    Print the alignment in a human-readable format.
    """
    print("".join("-" if i == "-" else i for i, _ in alignment))
    print("".join("-" if j == "-" else j for _, j in alignment))


if __name__ == "__main__":
    # Example usage
    x = "CAT"
    y = "CT"

    # Prompt user for scoring parameters
    print("Enter scoring parameters:")
    match_score = int(input("Match score (default 1): ") or 1)
    mismatch_penalty = int(input("Mismatch penalty (default -1): ") or -1)
    gap_penalty = int(input("Gap penalty (default -2): ") or -2)

    # Run the recursive alignment algorithm
    alignment, score = recursive_alignment(x, y, match_score, mismatch_penalty, gap_penalty)

    # Print the best alignment and score
    print("\nBest alignment:")
    print_alignment(x, y, alignment)
    print(f"Best score: {score}")
