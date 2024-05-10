import importlib.metadata
import io
import json
import sys
from typing import Any

import mypy.api


def run_mypy(path: str) -> str:
    stdout, stderr, returncode = mypy.api.run([path, "--output=json"])
    if returncode not in (0, 1):
        raise RuntimeError("mypy exited with non-zero status", returncode, stderr)

    return stdout


def mypy_output_to_sarif(mypy_output: str) -> dict[str, Any]:
    sarif_issues: list[dict[str, Any]] = []

    mypy_output_io = io.StringIO(mypy_output)
    for line in mypy_output_io:
        issue = json.loads(line)
        sarif_issues.append(
            {
                "ruleId": issue["code"],
                "level": issue["severity"],
                "message": {"text": issue["message"]},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": issue["file"]},
                            "region": {"startLine": issue["column"], "startColumn": issue["line"]},
                        }
                    }
                ],
            }
        )

    sarif_template = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "mypy",
                        "version": importlib.metadata.distribution("mypy").version,
                    }
                },
                "results": sarif_issues,
            }
        ],
    }
    return sarif_template


if __name__ == "__main__":
    filepath = sys.argv[1]
    mypy_output = run_mypy(filepath)
    print(json.dumps(mypy_output_to_sarif(mypy_output), indent=2))
