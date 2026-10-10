# Page Refresher

This started as a learning project: a simple app with several interfaces that all work the same way.

The real trigger was Tkinter. Tkinter runs everything on one main thread inside `mainloop()`, so a blocking Selenium call freezes the window. Pushing the work to a background thread fixes that, but you then have to hand results back to the main thread, because Tkinter widgets aren't thread-safe. I wanted to see how other GUI toolkits deal with the same problem.

Later I read about lazy imports, coming in Python 3.15 (PEP 810), and they reminded me of a workaround in this project. To keep a missing optional GUI dependency from breaking the whole CLI, I had hidden imports inside functions and given the Tkinter GUI its own console script, `page-refresher-tkinter`. Lazy imports looked like a cleaner fix, so I rewrote the project around them.

Before, the imports lived inside the functions that used them:

```python
# A separate console script for the GUI, plus imports hidden inside
# functions so a missing optional dependency wouldn't break the whole CLI.
def refresh(...):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    ...
```

Now they are ordinary top-level imports that load only when first used:

```python
# Top-level imports that load only when first used (PEP 810),
# so a single `page-refresher run <adapter>` command loads just that GUI.
lazy from selenium import webdriver
lazy from page_refresher.adapters.tkinter import main as run_tkinter
```

## Usage

Requires Python 3.15+.

```bash
uv sync
uv run page-refresher refresh --url https://example.com --delay 5 --refresh-count 10
uv run page-refresher run tkinter   # or: flet, nicegui
```
