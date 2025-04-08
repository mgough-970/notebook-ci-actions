# notebook-ci-actions

## Overview

This repository provides modular GitHub Actions to support the continuous integration (CI) of Jupyter notebooks. These actions are used to automate testing, validation, and quality assurance for notebooks in scientific and technical workflows.

It is a fork and enhancement of the [spacetelescope/notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions) repository, with additional support for **semantic versioning and tag-based action references**.

---

## Available Actions

The following reusable actions are available in this repository:

- **`ci_builder`**: Builds the runtime environment and installs required dependencies.
- **`ci_runner`**: Executes notebooks and monitors for runtime errors.
- **`ci_validation`**: Runs validation checks such as notebook structure and formatting.
- **`ci_scheduled`**: Schedules notebook runs on a recurring basis to ensure long-term stability.
- **`notebook_pep8check`**: Checks Python code in notebooks for PEP8 compliance.
- **`script_pep8check`**: Runs PEP8 checks on standalone Python scripts.
- **`broken_link_checker`**: Verifies that all hyperlinks in notebooks are valid and reachable.
- **`html_accessibility_check`**: Checks for accessibility issues in HTML outputs.
- **`update_dependabot_config_file`**: Automatically updates the `dependabot.yml` config if needed.

---

## Using These Actions

You can call these actions in your workflows using a tag reference (recommended) or branch reference (e.g., `main`).

### Example Workflow

```yaml
name: Notebook CI

on:
  pull_request:
    branches: [main]

jobs:
  run-notebooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install requirements
        run: |
          pip install -r requirements.txt

      - name: Execute notebooks
        uses: mgough-970/notebook-ci-actions/ci_runner@v1.0.0
```

## Contributing

Contributions are welcome! To propose an improvement or new feature:

1. Fork the repository  
2. Create a new branch (`feature/my-improvement`)  
3. Commit your changes  
4. Submit a pull request with context and motivation

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Maintainer**: [@mgough-970](https://github.com/mgough-970)  
**Based on**: [spacetelescope/notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions)

---

## Tagging and Releases

This repository supports **versioned GitHub Actions** using annotated tags (e.g., `v1.0.0`, `v1.1.0`) for stability and reproducibility.

### Why Use Tags?

Using tags instead of branch names like `main` ensures that:
- Your workflows are not affected by upstream changes.
- You can pin to a known-good version of an action.
- You gain better visibility into updates via GitHub’s release system.

### How to Reference Tags

```yaml
uses: mgough-970/notebook-ci-actions/ci_runner@v1.0.0
```
### How Releases Work

Each release:
- Is associated with a semantic version tag (e.g., `v1.0.0`)
- Includes a changelog of features, fixes, and updates
- Can be browsed under the **Releases** section on GitHub
