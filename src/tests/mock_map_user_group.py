import pytest


class MockMapUserGroup:
    @pytest.fixture
    def patch_map_user_group(self, monkeypatch):
        def patcher(path):
            async def mapper(x):
                return str(x)

            monkeypatch.setattr(path, "map_user", mapper)
            monkeypatch.setattr(path, "map_group", mapper)

        return patcher
