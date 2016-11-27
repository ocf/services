import pytest

from deploy import all_apps as _all_apps
from deploy import APPS_PATH


ALL_APPS = _all_apps()


@pytest.fixture
def apps_path():
    return APPS_PATH


@pytest.fixture(params=ALL_APPS)
def app(request):
    return request.param
