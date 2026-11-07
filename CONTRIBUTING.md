# Contributing to pymt5-linux

Thank you for your interest in contributing to **`pymt5-linux`**!
We welcome all contributions from algorithmic traders, quants, Python developers, and Linux enthusiasts.

## Development Workflow

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/renartacayle/pymt5-linux.git
   cd pymt5-linux
   ```

2. **Set up Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Run the Test Suite:**
   ```bash
   pytest -v
   ```

4. **Code Quality Standards:**
   - Format code with `black` and `ruff`.
   - Maintain 100% test passing rate.
   - Do not break backward compatibility with official `MetaTrader5` API signatures.

## Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit changes with clear, descriptive messages.
3. Push to your fork: `git push origin feature/your-feature-name`
4. Open a Pull Request on GitHub.
