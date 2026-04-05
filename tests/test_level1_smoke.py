from meine.app import MeineAI


async def test_app_mounts_to_home_screen() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.screen.id == "home-screen"


async def test_home_has_core_widgets() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.screen.query_one("#command-input") is not None
        assert app.screen.query_one("#output") is not None
