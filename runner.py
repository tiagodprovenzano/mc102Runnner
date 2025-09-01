import subprocess
import os
import requests
import zipfile
import io
from shutil import rmtree

SCRIPT = "labs/lab04.py"
TEST_DIR = "mc102Runnner/tests"
tarefa = "01" # exercicio que deseja puxar baixar os testes
BASE_URL = f"https://susy.ic.unicamp.br:9999/mc102/{tarefa}/aux/aux{tarefa}.zip"
OUTPUT_FOLDER = "mc102Runnner/tests"

def clear_folder(OUTPUT_FOLDER):
    if os.path.exists(OUTPUT_FOLDER):
        for filename in os.listdir(OUTPUT_FOLDER):
            file_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)

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
    # Limpando a pasta com os testes
    clear_folder(OUTPUT_FOLDER)
    # Baixando o ZIP dos testes
    print(f"Baixando {BASE_URL}...")
    response = requests.get(BASE_URL, verify=False)
    response.raise_for_status()

    # Extraindo o ZIP
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(OUTPUT_FOLDER)
        print(f"Testes extraidos para a pasta {OUTPUT_FOLDER}")

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