def NWScore(X, Y, match_score=1, mismatch_penalty=-1, gap_penalty=0):
    """
    Calculate the last line of the Needleman-Wunsch score matrix.
    """
    n = len(Y)
    # Initialize a 2-row scoring matrix
    Score = []
    for _ in range(2):
        Score.append([0] * (n + 1))

        
    # Initialize first row
    for j in range(1, n + 1):
        Score[0][j] = Score[0][j - 1] + gap_penalty

    # Compute scores
    for i in range(1, len(X) + 1):
        Score[1][0] = Score[0][0] + gap_penalty
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                match_or_mismatch = match_score
            else:
                match_or_mismatch = mismatch_penalty

            score_sub = Score[0][j - 1] + match_or_mismatch

            score_del = Score[0][j] + gap_penalty
            score_ins = Score[1][j - 1] + gap_penalty
            Score[1][j] = max(score_sub, score_del, score_ins)
        # Copy Score[1] to Score[0]
        Score[0] = Score[1][:]
    
    return Score[1]

def hirschberg_alignment(X, Y, match_score=1, mismatch_penalty=-1, gap_penalty=0):
    """
    Hirschberg algorithm for global alignment.
    """
    if len(X) == 0:
        # Align X to an empty string
        aligned_X = '-' * len(Y)
        aligned_Y = Y
    elif len(Y) == 0:
        # Align Y to an empty string
        aligned_X = X
        aligned_Y = '-' * len(X)
    elif len(X) == 1 or len(Y) == 1:
        # Base case, use NW
        aligned_X, aligned_Y = needleman_wunsch(X, Y, match_score, mismatch_penalty, gap_penalty)
    else:
        xmid = len(X) // 2
        
        # Compute score for partitions
        ScoreL = NWScore(X[:xmid], Y, match_score, mismatch_penalty, gap_penalty)
        reversed_X = X[xmid:][::-1]
        reversed_Y = Y[::-1]
        ScoreR = NWScore(reversed_X, reversed_Y, match_score, mismatch_penalty, gap_penalty)

        score_sums = []
        for j in range(len(Y) + 1):
            score_sum = ScoreL[j] + ScoreR[len(Y) - j]
            score_sums.append(score_sum)

        ymid = score_sums.index(max(score_sums))
                
        # Recurse
        left_aligned_X, left_aligned_Y = hirschberg_alignment(X[:xmid], Y[:ymid], match_score, mismatch_penalty, gap_penalty)
        right_aligned_X, right_aligned_Y = hirschberg_alignment(X[xmid:], Y[ymid:], match_score, mismatch_penalty, gap_penalty)
        
        aligned_X = left_aligned_X + right_aligned_X
        aligned_Y = left_aligned_Y + right_aligned_Y

    return aligned_X, aligned_Y


def needleman_wunsch(X, Y, match_score=1, mismatch_penalty=-1, gap_penalty=0):
    """
    Basic Needleman-Wunsch algorithm for short sequences.
    """
    m, n = len(X), len(Y)
    dp = []
    for _ in range(m + 1):
        dp.append([0] * (n + 1))

    
    # Initialize DP table
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + gap_penalty
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + gap_penalty
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i - 1][j - 1] + (match_score if X[i - 1] == Y[j - 1] else mismatch_penalty)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = max(match, delete, insert)
    
    # Traceback
    i, j = m, n
    aligned_X, aligned_Y = "", ""
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (match_score if X[i - 1] == Y[j - 1] else mismatch_penalty):
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + gap_penalty:
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = "-" + aligned_Y
            i -= 1
        else:
            aligned_X = "-" + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            j -= 1
    
    return aligned_X, aligned_Y


def print_alignment(X, Y, alignment):
    """
    Print the alignment in a human-readable format.
    """
    aligned_X, aligned_Y = alignment
    print("Alignment:")
    print(aligned_X)
    print(aligned_Y)

if __name__ == "__main__":
    # Input sequences
    X = input("Enter the first sequence: ")
    Y = input("Enter the second sequence: ")

    # Prompt user for scoring parameters
    print("Enter scoring parameters:")
    match_score = int(input("Match score (default 1): ") or 1)
    mismatch_penalty = int(input("Mismatch penalty (default -1): ") or -1)
    gap_penalty = int(input("Gap penalty (default -2): ") or -2)

    # Run the Hirschberg alignment algorithm
    alignment = hirschberg_alignment(X, Y, match_score, mismatch_penalty, gap_penalty)

    # Print the best alignment
    print_alignment(X, Y, alignment)
