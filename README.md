# ciopen

[![PyPI](https://img.shields.io/pypi/v/ciopen?color=blue&label=PyPI)](https://pypi.org/project/ciopen/)
![Python](https://img.shields.io/badge/python-%3E%3D3.10-brightgreen)
![GitHub Workflow](https://img.shields.io/github/actions/workflow/status/mel-cdn/ciopen/python.yml?label=build)


Quickly open CI pipelines from your Git repository.

`ciopen` lets you open your CI pipelines or repository pages straight from the terminal — works with GitHub, GitLab,
Bitbucket, Azure DevOps (and more coming soon!).

[Checkout ciopen on PyPI](https://pypi.org/project/ciopen/)

---

## ⚡ Features

Open CI pipeline on your default browser:

```bash
ciopen
```

---

## 💻 Installation

### Requirements:

- Python >=3.10
- Git installed and available in your PATH
- Access to the Git remote of the repository you want to open

### Using `pip`


```bash
pip install ciopen
```

### Using pip (editable / dev mode)
```bash
git clone https://github.com/mel-cdn/ciopen.git
cd ciopen
pipenv shell        # or activate your virtualenv
pip install -e .
```
---


## 🛠️ Usage Examples

Show helpful CLI documentation:

```bash
ciopen --help
# Usage: ciopen [OPTIONS] COMMAND [ARGS]...
...
```

Open your pipeline (default):

```bash
ciopen repo
# Quickly open CI pipelines from your Git repository.  
```

Check if it's going to work with diagnostics:

```bash
ciopen doctor
# ✅ Git installed
# ✅ Inside a Git repository
# ✅ Remote origin found
# ✅ CI Provider detected
# Detected provider: GitHub
# Repository: mel-cdn/ciopen
# Current branch: main
# Pipeline URL: https://github.com/mel-cdn/ciopen/actions
```

---

## 💡 Notes

- Works with HTTPS and SSH Git remotes.
- Detects CI provider automatically.
- Can be extended with more CI providers easily.
- Designed for casual, fast CLI usage.

## 🔮 Future Plans

- Add support for additional CI/CD providers (GitLab, Azure Pipelines, etc.)
- Add support for custom CI/CD providers e.g. CircleCI, Jenkins, AWS CodeBuild, etc.
- JSON output for scripts and automation
- Auto-detect Git branch and multiple pipelines
- Additional CLI shortcuts for common CI/CD tasks

---

## 🤝 Contributing

`ciopen` is open for contributions!

1. Fork the rep
2. Make your changes
3. Submit a Pull Request

All contributions are welcome — whether it’s new features, bug fixes, or improving docs.

---
Made with ❤️ for developers who love fast, terminal-first CI access.
