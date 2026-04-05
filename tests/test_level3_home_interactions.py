from meine.app import MeineAI


async def test_ctrl_d_toggles_directory_tree_visibility() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()

        directory_tree_container = app.screen.query_one("#directory-tree-container")
        assert directory_tree_container.has_class("-hidden")

        await pilot.press("ctrl+d")
        await pilot.pause()
        assert not directory_tree_container.has_class("-hidden")

        await pilot.press("ctrl+d")
        await pilot.pause()
        assert directory_tree_container.has_class("-hidden")


async def test_submit_clear_command_resets_input_and_updates_history() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()

        input_widget = app.screen.query_one("#command-input")
        history_before = len(app.HISTORY)

        await pilot.click("#command-input")
        await pilot.press("c", "l", "e", "a", "r")
        assert input_widget.value == "clear"

        await pilot.press("enter")
        await pilot.pause()

        assert input_widget.value == ""
        assert len(app.HISTORY) == history_before + 1
        assert app.HISTORY[-1] == "clear"
