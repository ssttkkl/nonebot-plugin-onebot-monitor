from unittest.mock import MagicMock, AsyncMock

import pytest


class FakeAsyncSession:
    def __init__(self):
        self.add = MagicMock()
        self.commit = AsyncMock()


class MockDataSource:
    @pytest.fixture(autouse=True)
    def mock_data_source(self, monkeypatch):
        fake_session = FakeAsyncSession()
        monkeypatch.setattr("nonebot_plugin_onebot_monitor.models.data_source.session", lambda: fake_session)
        print("mock data source")
