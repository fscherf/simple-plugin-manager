import pytest


def test_script_import():
    from simple_plugin_manager.plugin_manager import PluginManager
    from simple_plugin_manager import test_plugins

    plugin_manager = PluginManager()

    # load test plugin
    import_string = f'{test_plugins.__file__}::TestPlugin'

    plugin_manager.load([
        import_string,
    ])

    # run checks
    plugins = plugin_manager.get_plugins()

    assert len(plugins) == 1
    assert plugins[0].SECRET_STRING == test_plugins.TestPlugin.SECRET_STRING


def test_module_attribute_import():
    from simple_plugin_manager.plugin_manager import PluginManager
    from simple_plugin_manager.test_plugins import TestPlugin

    plugin_manager = PluginManager()

    # load test plugin
    plugin_manager.load([
        'simple_plugin_manager.test_plugins.TestPlugin',
    ])

    # run checks
    plugins = plugin_manager.get_plugins()

    assert len(plugins) == 1
    assert plugins[0].SECRET_STRING == TestPlugin.SECRET_STRING


# import errors ###############################################################
def test_script_import_error():
    from simple_plugin_manager.plugin_manager import PluginManager
    from simple_plugin_manager import test_plugins

    plugin_manager = PluginManager()

    # load test plugin
    with pytest.raises(ImportError):
        plugin_manager.load([
            f'{test_plugins.__file__}::Foo',
        ])

    # run checks
    plugins = plugin_manager.get_plugins()

    assert len(plugins) == 0


def test_module_attribute_import_error():
    from simple_plugin_manager.plugin_manager import PluginManager

    plugin_manager = PluginManager()

    # load test plugin
    with pytest.raises(ImportError):
        plugin_manager.load([
            'simple_plugin_manager.test_plugins.Foo',
        ])

    # run checks
    plugins = plugin_manager.get_plugins()

    assert len(plugins) == 0


# hook discovery ##############################################################
def test_hook_checks():
    from simple_plugin_manager import PluginManager as BasePluginManager
    from simple_plugin_manager.test_plugins import PlainTestPlugin, TestPlugin

    class InvalidTestPlugin(TestPlugin):
        pass

    class PluginManager(BasePluginManager):
        def check_hook(self, plugin, hook_name, hook):
            return not isinstance(plugin, InvalidTestPlugin)

    # setup plugins
    plugin_manager = PluginManager(hook_names=['handle_data'])

    plugin_manager.load([
        PlainTestPlugin,
        InvalidTestPlugin(),
        TestPlugin(),
    ])

    # run checks
    hooks = list(plugin_manager.iter_hooks(hook_name='handle_data'))

    assert len(hooks) == 1

    plugin, hook = hooks[0]

    assert isinstance(plugin, TestPlugin)
