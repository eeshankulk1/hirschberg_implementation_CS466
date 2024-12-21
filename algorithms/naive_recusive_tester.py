import time
import signal
import sys
from naive_recursive import recursive_alignment, print_alignment

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Execution exceeded time limit")

# Attach the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)

def run_test_case(x, y, match_score, mismatch_penalty, gap_penalty):
    """
    Run a single test case with timeout and runtime measurement.
    """
    try:
        signal.alarm(300)  # Set timeout to 300 seconds
        start_time = time.time()
        best_alignment, best_score = recursive_alignment(
            x, y, match_score=match_score, mismatch_penalty=mismatch_penalty, gap_penalty=gap_penalty
        )
        end_time = time.time()
        signal.alarm(0)  # Cancel the timeout

        runtime = end_time - start_time
        print(f"Test case for X='{x}', Y='{y}':")
        print("Best alignment:")
        print_alignment(x, y, best_alignment)
        print(f"Best score: {best_score}")
        # Print runtime in seconds to 6 float points
        print(f"Runtime: {runtime:.6f} seconds\n")

    except TimeoutException:
        print(f"Test case for X='{x}', Y='{y}' timed out after 5 mins seconds.\n")
    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
        sys.exit(1)


def test_brute_force():
    """
    Run 10 test cases with various alignments and edge cases.
    """
    # Define 10 test cases
    test_cases = [
        ("CAT", "CT", 1, -1, -2),        # Small strings
        ("GATTACA", "GCATGCU", 1, -1, -2),  # Medium strings with mismatches
        ("A", "T", 1, -1, -2),          # Single characters
        ("", "ACTG", 1, -1, -2),        # One empty string
        ("ACTG", "ACTG", 1, -1, -2),    # Identical strings
        ("AAAA", "AA", 2, -1, -2),      # Repeated characters
        ("AGGTAB", "GXTXAYB", 1, -1, -2),  # Long sequences with gaps
        ("A" * 5, "A" * 5, 1, -1, -2),  # Long identical strings
        ("ABC" * 3, "CBA" * 3, 1, -1, -2),  # Reversed strings
        ("GATTACAAC", "GCATGCUGCA", 1, -1, -2),  # Longer strings
    ]

    print("=== Brute Force Alignment Tester ===")
    for i, (x, y, match_score, mismatch_penalty, gap_penalty) in enumerate(test_cases):
        print(f"Running Test Case {i+1}...")
        run_test_case(x, y, match_score, mismatch_penalty, gap_penalty)


if __name__ == "__main__":
    try:
        test_brute_force()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
