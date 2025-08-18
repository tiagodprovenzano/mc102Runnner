import subprocess
import os

SCRIPT = "lab02.py"
TEST_DIR = "tests_2"

def run_test(input_path, output_path):
    with open(input_path, 'r') as infile, open(output_path, 'r') as outfile:
        expected_output = outfile.read().strip()
        
        result = subprocess.run(
            ['python3', SCRIPT],
            stdin=infile,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        actual_output = result.stdout.strip()
        return actual_output == expected_output, actual_output, expected_output

def main():
    test_cases = [f[:-3] for f in os.listdir(TEST_DIR) if f.endswith('.in')]
    test_cases.sort()

    for test in test_cases:
        input_file = os.path.join(TEST_DIR, test + ".in")
        output_file = os.path.join(TEST_DIR, test + ".out")

        if not os.path.exists(output_file):
            print(f"[SKIP] {test}: Missing .out file")
            continue

        passed, actual, expected = run_test(input_file, output_file)

        if passed:
            print(f"[PASS] {test}")
        else:
            print(f"[FAIL] {test}")
            print("Expected:")
            print(expected)
            print("Got:")
            print(actual)

if __name__ == "__main__":
    main()