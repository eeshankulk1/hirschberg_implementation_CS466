import time
import signal
import sys
from hirschberg_algorithm import hirschberg_alignment, print_alignment

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

        # Progress tracking for the longest test case
        progress_interval = 1  # Update progress every second
        progress_start = time.time()

        def show_progress():
            elapsed = time.time() - progress_start
            print(f"Progress: {elapsed:.2f} seconds elapsed for test case '{x}' vs '{y}'...", end="\r", flush=True)

        # Run the alignment and track progress
        while True:
            try:
                best_alignment = hirschberg_alignment(
                    x, y, match_score=match_score, mismatch_penalty=mismatch_penalty, gap_penalty=gap_penalty
                )
                break
            except TimeoutException:
                raise TimeoutException("Execution exceeded time limit")
            finally:
                # Update progress every interval
                if time.time() - progress_start >= progress_interval:
                    show_progress()
                    progress_start = time.time()

        end_time = time.time()
        signal.alarm(0)  # Cancel the timeout

        runtime = end_time - start_time
        print(f"Test case for X='{x}', Y='{y}':")
        print("Best alignment:")
        print_alignment(x, y, best_alignment)
        print(f"Runtime: {runtime:.6f} seconds\n")

    except TimeoutException:
        print(f"Test case for X='{x}', Y='{y}' timed out after 5 minutes.\n")
    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
        sys.exit(1)

def test_hirschberg_alignment():
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
        ("GATTACA" * 2, "GCATGCU" * 2, 1, -1, -2),  # Longer strings
    ]

    print("=== Hirschberg Alignment Tester ===")
    for i, (x, y, match_score, mismatch_penalty, gap_penalty) in enumerate(test_cases):
        print(f"Running Test Case {i+1}...")
        run_test_case(x, y, match_score, mismatch_penalty, gap_penalty)

if __name__ == "__main__":
    try:
        test_hirschberg_alignment()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
