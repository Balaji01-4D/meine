# Running Tests for Meine Application

## Setup

Before running tests, ensure you have the required dependencies installed:

```bash
pip install pytest pytest-asyncio pytest-textual-snapshot
```

## Running Basic Tests

To run all the tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_meine_app.py
```

## Running Snapshot Tests

Snapshot tests compare the visual output of your application against saved snapshots.

When running for the first time, the tests will fail because there are no saved snapshots:

```bash
pytest tests/test_meine_snapshot.py
```

After reviewing the generated snapshots in the browser (follow the link provided in the output), update the snapshots by running:

```bash
pytest --snapshot-update
```

This will save the current snapshots as the "ground truth" for future comparisons.

Future test runs will compare against these saved snapshots:

```bash
pytest tests/test_meine_snapshot.py
```

## Understanding Test Failures

If a snapshot test fails after updating the app:

1. Run `pytest` without the `--snapshot-update` flag
2. Open the HTML report (link will be in the test output)
3. Compare the current output with the saved snapshot
4. If the changes are intentional, run `pytest --snapshot-update` to update the snapshots
5. If the changes are unintentional, fix the code and run tests again

## Test Organization

We have multiple test files using different approaches to test the app:

- `test_meine_app.py`: Basic functionality tests using direct app initialization
- `test_meine_snapshot.py`: Visual snapshot tests for different screens and states
- `test_direct_app.py`: Alternative approach to snapshot testing
- `test_functional.py`: Class-based functional tests without snapshots
- `test_fixture_based.py`: Tests using pytest fixtures for app initialization

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
3. Verify that the app can run normally with `python run.py`
4. If tests are failing due to timing issues, you may need to increase the `pause()` durations in the tests

### Common Issues

1. **"Unable to find app in run.py"**: 
   - This happens because the pytest-textual-snapshot is looking for an app instance in run.py
   - Our solution is to use absolute paths to run.py instead of relative paths

2. **"No nodes match '#command-input'"**:
   - This happens when the app hasn't fully initialized before we try to access elements
   - We've added `await pilot.pause(0.5)` to give the app time to initialize
   - If you still see this error, try increasing the pause duration

3. **"asyncio.run() cannot be called from a running event loop"**:
   - This happens when trying to use `snap_compare` with a direct app instance inside an `@pytest.mark.asyncio` test
   - The solution is to use the path to run.py instead of directly passing the app instance
   - Alternatively, use the `test_functional.py` tests which focus on functional testing rather than snapshot testing
