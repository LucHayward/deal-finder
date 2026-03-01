# uv Primer

`uv` is a fast Python package manager written in Rust. It replaces `pip`, `venv`, `pyenv`, and `poetry` with a single tool.

## Why uv?

- **Speed**: 10-100x faster than pip
- **All-in-one**: Manages Python versions, virtual environments, and packages
- **Lockfiles**: Reproducible builds with `uv.lock`
- **No config needed**: Just works

## How uv Picks a Python Version

uv looks for Python in this order:

1. `.python-version` file in the project
2. `pyproject.toml` `requires-python` field
3. Already installed Python versions (via mise, pyenv, system)
4. Downloads one automatically if needed

## Virtual Environment

uv automatically creates `.venv/` when you run `uv add` or `uv run`. This isolates packages from your system Python.

```
project/
├── .venv/           # Isolated Python environment
│   ├── bin/python   # Python interpreter
│   └── lib/         # Installed packages
├── pyproject.toml   # Dependencies declared here
└── uv.lock          # Exact versions locked
```

## Common Commands

| Command | What it does |
|---------|--------------|
| `uv init` | Create new project |
| `uv add <pkg>` | Install a package |
| `uv remove <pkg>` | Uninstall a package |
| `uv run <script>` | Run with venv activated |
| `uv sync` | Install from lockfile |
| `uv lock` | Update lockfile |
| `uv python list` | Show available Python versions |
| `uv python install 3.11` | Install a Python version |

## vs Traditional Workflow

**Old way:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4 requests
python script.py
```

**uv way:**
```bash
uv add beautifulsoup4 requests
uv run script.py
```

## Running Scripts

```bash
# With uv (auto-activates venv)
uv run script.py

# Or activate manually
source .venv/bin/activate
python script.py
```
