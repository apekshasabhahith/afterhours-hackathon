import json
import requests
from pathlib import Path
from datetime import datetime

API_URL = "http://127.0.0.1:8002/analyze"

BASE_DIR = Path(__file__).resolve().parent
TEST_FILE = BASE_DIR / "test_cases.json"
RESULT_FILE = BASE_DIR / "test_results" / "results.json"


def load_test_cases():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("test_cases", "cases", "tests"):
            if isinstance(data.get(key), list):
                return data[key]

    raise ValueError("Could not find a list of test cases in test_cases.json")


def main():
    test_cases = load_test_cases()
    results = []

    print(f"\nScamBreaker: Running {len(test_cases)} test cases\n")

    for index, case in enumerate(test_cases, start=1):
        text = case.get("text", case.get("message", ""))

        if not text:
            print(f"Test {index}: SKIPPED — no text/message field")
            continue

        payload = {
            "text": text,
            "ts": float(index),
            "call_id": f"automated_test_{index}"
        }

        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()

            print(f"Test {index}: {case.get('name', case.get('id', 'Unnamed'))}")
            print(f"  Level: {result.get('level')}")
            print(f"  Score: {result.get('score')}")
            print(f"  Stage: {result.get('stage')}")
            print("  Status: PASSED (API responded successfully)\n")

            results.append({
                "test_number": index,
                "input": case,
                "response": result,
                "http_status": response.status_code
            })

        except requests.RequestException as error:
            print(f"Test {index}: FAILED — {error}\n")

    RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"Completed. Successful API responses: {len(results)}/{len(test_cases)}")
    print(f"Results saved to: {RESULT_FILE}")


if __name__ == "__main__":
    main()