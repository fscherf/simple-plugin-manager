def test_module_import():
    from simple_plugin_manager.loading import load

    json = load('json')

    assert hasattr(json, 'dumps')


def test_loader():
    import inspect

    from simple_plugin_manager import test_plugins, Loader

    # setup
    loader = Loader()

    TestPlugin = loader.load(
        'simple_plugin_manager.test_plugins.TestPlugin',
    )

    ArgumentParser = loader.load(
        'argparse.ArgumentParser',
    )

    dumps = loader.load(
        'json.dumps',
    )

    # run checks
    assert inspect.isclass(TestPlugin)
    assert TestPlugin.SECRET_STRING == test_plugins.TestPlugin.SECRET_STRING

    assert inspect.isclass(ArgumentParser)
    assert hasattr(ArgumentParser, 'parse_args')

    assert inspect.isfunction(dumps)


def test_loader_caching():
    from simple_plugin_manager import Loader

    loader = Loader()

    assert loader.get_import_strings() == []

    # first load
    TestPlugin1 = loader.load(
        'simple_plugin_manager.test_plugins.TestPlugin',
    )

    assert loader.get_import_strings() == [
        'simple_plugin_manager.test_plugins.TestPlugin',
    ]

    # second load
    TestPlugin2 = loader.load(
        'simple_plugin_manager.test_plugins.TestPlugin',
    )

    assert loader.get_import_strings() == [
        'simple_plugin_manager.test_plugins.TestPlugin',
    ]

    assert TestPlugin1 is TestPlugin2
