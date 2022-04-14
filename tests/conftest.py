from pytest import fixture


def pytest_addoption(parser):
    parser.addoption("--test_config", action="store")


@fixture(scope="session")
def name(request):
    name_value = request.config.option.test_config
    print(name_value)
    return True
