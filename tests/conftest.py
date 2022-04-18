""" The module used for setting up pytest command line arguments"""

from pytest import fixture

def pytest_addoption(parser):
    """pass a parser object"""
    parser.addoption("--test_config", action="store")


@fixture(scope="session")
def name(request):
    """Fixture function"""
    name_value = request.config.option.test_config
    print(name_value)
    return True
