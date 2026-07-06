# Contributing to agent-spark

Thanks for considering contributing! ??

## How to Contribute

### 1. Find or Open an Issue
Check [existing issues](https://github.com/nousresearch/agent-spark/issues) or open a new one. Label suggestions:

- `?? bug` ??something doesn't work
- `??enhancement` ??new feature or improvement
- `?? i18n` ??translations or locale improvements
- `?? docs` ??documentation

### 2. Fork & Branch
```bash
git clone https://github.com/YOUR_USERNAME/agent-spark.git
cd agent-spark
git checkout -b feat/your-feature-name
```

### 3. Set Up Dev Environment
```bash
pip install -e ".[dev]"
```

### 4. Make Changes
- **Filter engine additions**: add to `agent-spark/filter/five_layer_filter.py`
- **New mature products**: add to the `MATURE_PRODUCTS` list in the filter
- **Prompt improvements**: edit `agent-spark/prompts/` files (bilingual)
- **Documentation**: edit `README.md` (keep it English-first, bilingual format)

### 5. Run Tests
```bash
pytest tests/ -v
```

All tests must pass. Add tests for new functionality.

### 6. Commit & Push
```bash
git add .
git commit -m "feat: concise description of your change"
git push origin feat/your-feature-name
```

### 7. Open a Pull Request
Link to the issue in your PR description. Include screenshots or demo output if relevant.

## Code Style
- Python: follow PEP 8
- Docstrings: Google style
- Chinese text: always paired with English
- Filter engine: keep it stdlib-only (no external dependencies)

## Code of Conduct
Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be excellent to each other.

## Good First Issues
- Add more products to `MATURE_PRODUCTS` in the filter
- Improve Chinese bigram matching edge cases
- Write a web-search integration module (optional dep)
- Create a Streamlit UI for visual demo
- Translate prompts to Japanese/Korean/Spanish

---

*By contributing, you agree that your contributions will be licensed under the MIT License.*

