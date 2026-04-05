from meine.app import (
    MeineAI,
    HELP_SCREEN_ID,
    SETTINGS_SCREEN_ID,
    SYSTEM_UTILS_SCREEN_ID,
)


async def test_ctrl_s_toggles_settings_screen() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()

        await pilot.press("ctrl+s")
        await pilot.pause()
        assert app.screen.id == SETTINGS_SCREEN_ID

        await pilot.press("ctrl+s")
        await pilot.pause()
        assert app.screen.id == "home-screen"


async def test_ctrl_k_toggles_help_screen() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()

        app.key_ctrl_k()
        await pilot.pause()
        assert app.screen.id == HELP_SCREEN_ID

        app.key_ctrl_k()
        await pilot.pause()
        assert app.screen.id == "home-screen"


async def test_ctrl_m_toggles_system_utils_screen() -> None:
    app = MeineAI()

    async with app.run_test() as pilot:
        await pilot.pause()

        await pilot.press("ctrl+m")
        await pilot.pause()
        assert app.screen.id == SYSTEM_UTILS_SCREEN_ID

        await pilot.press("ctrl+m")
        await pilot.pause()
        assert app.screen.id == "home-screen"
