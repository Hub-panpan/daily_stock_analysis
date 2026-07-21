# -*- coding: utf-8 -*-
"""Regression tests for scheduled mode stock selection behavior."""

import json
import logging
import os
import socket
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

_ENV_BEFORE_MAIN_IMPORT = dict(os.environ)
import main
from src.brokers.futu.portfolio import FutuPortfolioError
from src.config import Config

_MAIN_IMPORT_ENV_ADDITIONS = frozenset(set(os.environ) - set(_ENV_BEFORE_MAIN_IMPORT))
_MAIN_IMPORT_ENV_OVERRIDES = {
    key: value
    for key, value in _ENV_BEFORE_MAIN_IMPORT.items()
    if os.environ.get(key) != value
}


def _api_app_stub_modules():
    """sys.modules entries so ``start_api_server`` can ``from api.app import app``
    without importing the real (heavy) app tree in these isolated unit tests.

    ``start_api_server`` imports the ASGI app object in the calling thread so the
    import stays out of the uvicorn startup probe window; these control-flow tests
    stub it the same way they already stub uvicorn.
    """
    import types

    api_pkg = types.ModuleType("api")
    api_app_mod = types.ModuleType("api.app")
    api_app_mod.app = SimpleNamespace()
    api_pkg.app = api_app_mod
    return {"api": api_pkg, "api.app": api_app_mod}


class _DummyConfig(SimpleNamespace):
    def validate(self):
        return []


class MainScheduleModeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.env_path = Path(self.temp_dir.name) / ".env"
        self.env_path.write_text("STOCK_LIST=600519\n", encoding="utf-8")
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        self.env_patch = patch.dict(os.environ, {"ENV_FILE": str(self.env_path)}, clear=False)
        self.env_patch.start()
        Config.reset_instance()
        root_logger = logging.getLogger()
        self._original_root_handlers = list(root_logger.handlers)
        self._original_root_level = root_logger.level

    def tearDown(self) -> None:
        root_logger = logging.getLogger()
        current_handlers = list(root_logger.handlers)
        for handler in current_handlers:
            if handler not in self._original_root_handlers:
                root_logger.removeHandler(handler)
                try:
                    handler.close()
                except Exception:
                    pass
        root_logger.setLevel(self._original_root_level)
        os.chdir(self.original_cwd)
        Config.reset_instance()
        self.env_patch.stop()
        for key in _MAIN_IMPORT_ENV_ADDITIONS:
            os.environ.pop(key, None)
        for key, value in _MAIN_IMPORT_ENV_OVERRIDES.items():
            os.environ[key] = value
        self.temp_dir.cleanup()

    def _make_args(self, **overrides):
        defaults = {
            "debug": False,
            "stocks": None,
            "portfolio": None,
            "webui": False,
            "webui_only": False,
            "serve": False,
            "serve_only": False,
            "host": None,
            "port": None,
            "backtest": False,
            "market_review": False,
            "schedule": False,
            "no_run_immediately": False,
            "no_notify": False,
            "check_notify": False,
            "no_market_review": False,
            "dry_run": False,
            "workers": 1,
            "force_run": False,
            "single_notify": False,
            "no_context_snapshot": False,
        }
        defaults.update(overrides)
        return SimpleNamespace(**defaults)

    def _make_config(self, **overrides):
        defaults = {
            "log_dir": self.temp_dir.name,
            "webui_enabled": False,
            "webui_host": "127.0.0.1",
            "webui_port": 8000,
            "dingtalk_stream_enabled": False,
            "feishu_stream_enabled": False,
            "schedule_enabled": False,
            "schedule_time": "18:00",
            "schedule_run_immediately": True,
            "run_immediately": True,
            "agent_event_monitor_enabled": False,
            "agent_event_alert_rules_json": "",
            "agent_event_monitor_interval_minutes": 5,
            "daily_market_context_enabled": True,
        }
        defaults.update(overrides)
        return _DummyConfig(**defaults)

    def test_daily_market_context_target_date_routes_jp_kr_calendars(self) -> None:
        current_time = datetime(2026, 5, 7, 0, 30, tzinfo=timezone.utc)
        calls = []

        def resolve_effective_date(market, *, current_time=None):
            calls.append((market, current_time))
            return date(2026, 5, 7)

        with patch(
            "src.core.trading_calendar.get_effective_trading_date",
            side_effect=resolve_effective_date,
        ):
            self.assertEqual(
                main._resolve_daily_market_context_target_date("jp", current_time),
                date(2026, 5, 7),
            )
            self.assertEqual(
                main._resolve_daily_market_context_target_date("kr", current_time),
                date(2026, 5, 7),
            )
            self.assertEqual(
                main._resolve_daily_market_context_target_date("jp,kr", current_time),
                date(2026, 5, 7),
            )

        self.assertEqual(
            calls,
            [
                ("jp", current_time),
                ("kr", current_time),
                ("jp", current_time),
            ],
        )

    def test_compute_trading_day_filter_supports_comma_list_regions(self) -> None:
        args = self._make_args()
        config = self._make_config(
            trading_day_check_enabled=True,
            market_review_enabled=True,
            market_review_region="jp,kr",
            database_path=str(Path(self.temp_dir.name) / "stock_analysis.db"),
        )

        stock_codes = ["cn-stock", "jp-stock", "kr-stock", "us-stock", "none-stock"]

        with patch(
            "src.core.trading_calendar.get_market_for_stock",
            side_effect=lambda code: {"cn-stock": "cn", "jp-stock": "jp", "kr-stock": "kr", "us-stock": "us"}.get(code),
        ), patch("src.core.trading_calendar.get_open_markets_today", return_value={"jp", "kr"}):
            filtered_codes, effective_region, should_skip_all = main._compute_trading_day_filter(
                config,
                args,
                stock_codes,
            )

        self.assertEqual(filtered_codes, ["jp-stock", "kr-stock", "none-stock"])
        self.assertEqual(effective_region, "jp,kr")
        self.assertFalse(should_skip_all)

    def test_public_webui_bind_warns_when_auth_is_disabled(self) -> None:
        with patch("src.auth.is_auth_enabled", return_value=False), \
             patch("main.logger.warning") as warning_log:
            main._warn_if_public_webui_without_auth("0.0.0.0")

        warning_log.assert_called_once()
        self.assertIn("WEBUI_HOST=%s", warning_log.call_args.args[0])
        self.assertEqual(warning_log.call_args.args[1], "0.0.0.0")

    def test_loopback_webui_bind_does_not_warn_when_auth_is_disabled(self) -> None:
        with patch("src.auth.is_auth_enabled", return_value=False), \
             patch("main.logger.warning") as warning_log:
            main._warn_if_public_webui_without_auth("127.0.0.1")

        warning_log.assert_not_called()

    def test_web_service_bind_uses_config_when_cli_omits_host_and_port(self) -> None:
        args = self._make_args(host=None, port=None)
        config = self._make_config(webui_host="127.0.0.1", webui_port=18000)

        host, port = main._resolve_web_service_bind(args, config)

        self.assertEqual(host, "127.0.0.1")
        self.assertEqual(port, 18000)

    def test_web_service_bind_keeps_explicit_cli_host_and_port(self) -> None:
        args = self._make_args(host="0.0.0.0", port=8000)
        config = self._make_config(webui_host="127.0.0.1", webui_port=18000)

        host, port = main._resolve_web_service_bind(args, config)

        self.assertEqual(host, "0.0.0.0")
        self.assertEqual(port, 8000)

    def test_serve_only_uses_config_bind_when_cli_omits_host_and_port(self) -> None:
        args = self._make_args(serve_only=True)
        config = self._make_config(webui_enabled=False, webui_host="127.0.0.1", webui_port=18000)
        observed_bind = []

        def fake_start_api_server(host, port, config):
            observed_bind.append((host, port))

        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}, clear=False), \
             patch("main.parse_arguments", return_value=args), \
             patch("main.get_config", return_value=config), \
             patch("main.prepare_webui_frontend_assets", return_value=True), \
             patch("main.start_api_server", side_effect=fake_start_api_server), \
             patch("main.start_bot_stream_clients"), \
             patch("main.time.sleep", side_effect=KeyboardInterrupt):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(observed_bind, [("127.0.0.1", 18000)])

    def test_serve_only_keeps_explicit_cli_bind_over_config(self) -> None:
        args = self._make_args(serve_only=True, host="0.0.0.0", port=8000)
        config = self._make_config(webui_enabled=False, webui_host="127.0.0.1", webui_port=18000)
        observed_bind = []

        def fake_start_api_server(host, port, config):
            observed_bind.append((host, port))

        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}, clear=False), \
             patch("main.parse_arguments", return_value=args), \
             patch("main.get_config", return_value=config), \
             patch("main.prepare_webui_frontend_assets", return_value=True), \
             patch("main.start_api_server", side_effect=fake_start_api_server), \
             patch("main.start_bot_stream_clients"), \
             patch("main.time.sleep", side_effect=KeyboardInterrupt):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(observed_bind, [("0.0.0.0", 8000)])

    def test_start_api_server_fails_before_thread_when_port_is_busy(self) -> None:
        config = self._make_config(log_level="INFO")

        class BusySocket:
            def bind(self, address):
                raise OSError("address already in use")

            def close(self):
                pass

        with patch("socket.socket", return_value=BusySocket()) as socket_factory, \
             patch("threading.Thread") as thread_cls:
            with self.assertRaises(RuntimeError) as caught:
                main.start_api_server("127.0.0.1", 8000, config)

        socket_factory.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIn("127.0.0.1:8000", str(caught.exception))
        thread_cls.assert_not_called()

    def test_start_api_server_fails_when_uvicorn_background_startup_fails(self) -> None:
        config = self._make_config(log_level="INFO")

        class _FakeUvicornServer:
            def __init__(self, config):
                self.config = config
                self.started = False

            def run(self) -> None:
                raise RuntimeError("lifespan bootstrap failed")

        class _FakeUvicornConfig:
            def __init__(self, *args, **kwargs):
                pass

        class _FakeUvicornModule:
            Config = _FakeUvicornConfig

            Server = _FakeUvicornServer

        class _UnusedSocket:
            def bind(self, address):
                pass

            def close(self):
                pass

        with patch("socket.socket", return_value=_UnusedSocket()), \
             patch.dict(
                 "sys.modules",
                 {"uvicorn": _FakeUvicornModule(), **_api_app_stub_modules()},
             ):

            with self.assertRaises(RuntimeError) as caught:
                main.start_api_server("127.0.0.1", 8000, config)

        self.assertIn("lifespan bootstrap failed", str(caught.exception))

    def test_start_api_server_compatible_with_uvicorn_install_signal_handlers_method(self) -> None:
        config = self._make_config(log_level="INFO")

        class _CompatServer:
            instance = None

            def __init__(self, config):
                type(self).instance = self
                self.config = config
                self.started = False
                self.install_signal_handlers = self._install_signal_handlers

            def _install_signal_handlers(self) -> None:
                return None

            def run(self) -> None:
                self.started = True

        class _CompatConfig:
            def __init__(self, *args, **kwargs):
                if "install_signal_handlers" in kwargs:
                    raise TypeError("install_signal_handlers is unsupported")

        class _UnusedSocket:
            def bind(self, address):
                pass

            def close(self):
                pass

        with patch("socket.socket", return_value=_UnusedSocket()), \
             patch.dict(
                 "sys.modules",
                 {
                     "uvicorn": SimpleNamespace(Config=_CompatConfig, Server=_CompatServer),
                     **_api_app_stub_modules(),
                 },
             ):
            main.start_api_server("127.0.0.1", 8000, config)

        self.assertIsNotNone(_CompatServer.instance)
        self.assertTrue(callable(_CompatServer.instance.install_signal_handlers))
        self.assertTrue(_CompatServer.instance.started)

    def test_schedule_mode_ignores_cli_stock_snapshot(self) -> None:
        args = self._make_args(schedule=True, stocks="600519,000001")
        config = self._make_config(schedule_enabled=False)
        scheduled_call = {}

        def fake_run_with_schedule(
            task,
            schedule_time,
            run_immediately,
            background_tasks=None,
            schedule_time_provider=None,
        ):
            scheduled_call["schedule_time"] = schedule_time
            scheduled_call["run_immediately"] = run_immediately
            scheduled_call["background_tasks"] = background_tasks or []
            scheduled_call["resolved_schedule_time"] = (
                schedule_time_provider() if schedule_time_provider is not None else None
            )
            task()

        with patch("main.parse_arguments", return_value=args), \
             patch("main.get_config", return_value=config), \
             patch("main._reload_runtime_config", return_value=config), \
             patch("main._build_schedule_time_provider", return_value=lambda: "18:00"), \
             patch("main.setup_logging"), \
             patch("main.run_full_analysis") as run_full_analysis, \
             patch("main.logger.warning") as warning_log, \
             patch("src.scheduler.run_with_schedule", side_effect=fake_run_with_schedule):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            scheduled_call,
            {
                "schedule_time": "18:00",
                "run_immediately": True,
                "background_tasks": [],
                "resolved_schedule_time": "18:00",
            },
        )
        run_full_analysis.assert_called_once_with(config, args, None)
        warning_log.assert_any_call(
            "定时模式下检测到 --stocks 参数；计划执行将忽略启动时股票快照，并在每次运行前重新读取最新的 STOCK_LIST。"
        )

    def test_standalone_run_resolves_stocks_before_run_full_analysis(self) -> None:
        args = self._make_args(stocks="005930")
        config = self._make_config(run_immediately=True)

        with patch("main.parse_arguments", return_value=args), \
             patch("main.get_config", return_value=config), \
             patch("main.setup_logging"), \
             patch("main.run_full_analysis") as run_full_analysis:
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        run_full_analysis.assert_called_once()
        _, _, stock_codes = run_full_analysis.call_args.args
        self.assertEqual(stock_codes, ["005930.KS"])

    def test_standalone_futu_portfolio_failure_returns_nonzero(self) -> None:
        args = self._make_args(portfolio="futu")
        config = self._make_config(run_immediately=True)
        error = FutuPortfolioError("OpenD unavailable")

        with (
            patch("main.parse_arguments", return_value=args),
            patch("main.get_config", return_value=config),
            patch("main.setup_logging"),
            patch("main._refresh_stock_index_cache_for_analysis"),
            patch(
                "src.brokers.futu.portfolio.load_futu_stock_codes",
                side_effect=error,
            ) as loader,
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        loader.assert_called_once_with()

    def test_standalone_futu_portfolio_success_returns_zero(self) -> None:
        args = self._make_args(portfolio="futu")
        config = self._make_config(run_immediately=True)

        with (
            patch("main.parse_arguments", return_value=args),
            patch("main.get_config", return_value=config),
            patch("main.setup_logging"),
            patch("main._refresh_stock_index_cache_for_analysis"),
            patch(
                "src.brokers.futu.portfolio.load_futu_stock_codes",
                return_value=["AAPL"],
            ) as loader,
            patch(
                "main._compute_trading_day_filter",
                return_value=([], "", True),
            ),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        loader.assert_called_once_with()

    def test_standalone_futu_downstream_failure_keeps_existing_exit_semantics(self) -> None:
        args = self._make_args(portfolio="futu")
        config = self._make_config(run_immediately=True)

        with (
            patch("main.parse_arguments", return_value=args),
            patch("main.get_config", return_value=config),
            patch("main.setup_logging"),
            patch("main._refresh_stock_index_cache_for_analysis"),
            patch(
                "src.brokers.futu.portfolio.load_futu_stock_codes",
                return_value=["AAPL"],
            ) as loader,
            patch(
                "main._compute_trading_day_filter",
                side_effect=RuntimeError("calendar unavailable"),
            ),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        loader.assert_called_once_with()

