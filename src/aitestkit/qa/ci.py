from pathlib import Path

class CIGenerator:
    """Automates GitHub Actions and CI/CD workflow pipeline file generation."""

    GITHUB_ACTION_TEMPLATE = """name: AITestKit Automated AI QA Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  ai-qa-evaluation:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Codebase
      uses: actions/checkout@v3

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install AITestKit & Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install .

    - name: Run System Diagnostics Doctor
      run: |
        aitest doctor

    - name: Run Framework Auto-Scan
      run: |
        aitest scan

    - name: Execute Automated QA Test Suite
      run: |
        aitest test --threshold 0.75

    - name: Generate Executive Summary Report
      run: |
        aitest report --format md
"""

    @classmethod
    def generate_github_action(cls, output_path: str = ".github/workflows/aitestkit_qa.yml") -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(cls.GITHUB_ACTION_TEMPLATE)

        return str(path)