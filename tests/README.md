# Running Tests for Meine Application

## Setup

Before running tests, ensure you have the required dependencies installed:

```bash
uv pip install pytest pytest-asyncio
```

## Running Basic Tests

To run all the tests:

```bash
uv run pytest
```

To run a specific test file:

```bash
uv run pytest tests/test_meine_app.py
```

## Minimal Atomic Test Levels

These files are designed for commit-by-level progress:

- Level 1: `tests/test_level1_smoke.py`
- Level 2: `tests/test_level2_navigation_keys.py`
- Level 3: `tests/test_level3_home_interactions.py`

Run and commit each level independently:

```bash
uv run pytest -q tests/test_level1_smoke.py
git add tests/test_level1_smoke.py
git commit -m "tests: add level 1 smoke coverage"

uv run pytest -q tests/test_level2_navigation_keys.py
git add tests/test_level2_navigation_keys.py
git commit -m "tests: add level 2 navigation key coverage"

uv run pytest -q tests/test_level3_home_interactions.py
git add tests/test_level3_home_interactions.py
git commit -m "tests: add level 3 home interaction coverage"
```

## Understanding Test Failures

If a test fails after updates:

1. Re-run the failing file only: `uv run pytest -q tests/<file>.py`
2. Inspect the assertion and trace to confirm whether behavior changed intentionally
3. If the change is intentional, update or replace the affected test with a reliable assertion
4. If the change is unintentional, fix the app code and re-run `uv run pytest -q`

## Test Organization

We have multiple test files using different approaches to test the app:

- `test_meine_app.py`: Basic functionality tests using direct app initialization
- `test_functional.py`: Class-based functional tests without snapshots
- `test_fixture_based.py`: Tests using pytest fixtures for app initialization
- `test_level1_smoke.py`, `test_level2_navigation_keys.py`, `test_level3_home_interactions.py`: Atomic, commit-by-level reliable tests

If you encounter issues with one testing approach, try another. The fixture-based approach (`test_fixture_based.py`) is often the most reliable for functional testing.

## Testing Limitations

When testing Textual apps, there are a few limitations to be aware of:

1. **Command Navigation**: The command handling in the app doesn't always work in test mode. 
   - When the app is running in a real terminal, typing commands like "settings" and pressing enter works
   - In test mode, the commands are typed correctly but they don't trigger navigation
   - Our workaround: We directly push screens using `app.push_screen()` instead of relying on command input

2. **Asyncio Events**: Some events might not be triggered or processed as expected in test mode.
   - This is why we use longer pause durations to ensure events have time to propagate

3. **UI Rendering**: Some UI elements might behave differently in test mode vs. real terminal

The updated tests now account for these limitations, using direct screen manipulation where necessary.

## Troubleshooting

If you encounter issues with running tests:

1. Ensure all dependencies are installed
2. Check that you're running Python 3.11+ (required by the app)
3. Verify that the app can run normally with `uv run meine`
4. If tests are failing due to timing issues, you may need to increase the `pause()` durations in the tests

### Common Issues

1. **"No nodes match '#command-input'"**:
   - This happens when the app hasn't fully initialized before we try to access elements
   - We've added `await pilot.pause(0.5)` to give the app time to initialize
   - If you still see this error, try increasing the pause duration

2. **Flaky key shortcuts in focused inputs**:
   - Some Ctrl shortcuts can be consumed by the focused input widget in headless tests
   - Prefer stable interaction patterns (screen handlers or non-conflicting keys) when assertions are flaky
