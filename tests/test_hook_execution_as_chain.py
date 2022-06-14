def test_basic_execution_as_chain():
    from simple_plugin_manager.test_plugins import TestPlugin
    from simple_plugin_manager import PluginManager

    # setup plugins
    state = []
    data = 'foo'
    plugin_manager = PluginManager(hook_names=['handle_data'])

    plugin_manager.load([
        TestPlugin(name='plugin-1', state=state),
        TestPlugin(name='plugin-2', state=state),
        TestPlugin(name='plugin-3', state=state),
    ])

    # run hook 'handle_data'
    return_value = plugin_manager.run_hook_as_chain(
        hook_name='handle_data',
        hook_arg=data,
    )

    # run checks
    assert return_value is 'foo'

    assert state == [
        ('plugin-1', 'foo'),
        ('plugin-2', 'foo'),
        ('plugin-3', 'foo'),
    ]


def test_bubbling():
    from simple_plugin_manager.test_plugins import TestPlugin
    from simple_plugin_manager import PluginManager

    # setup plugins
    state = []
    data = 'foo'
    plugin_manager = PluginManager(hook_names=['handle_data'])

    plugin_manager.load([
        TestPlugin(name='plugin-1', state=state),
        TestPlugin(name='plugin-2', state=state, bubble_up=False),
        TestPlugin(name='plugin-3', state=state),
    ])

    # run hook 'handle_data'
    return_value = plugin_manager.run_hook_as_chain(
        hook_name='handle_data',
        hook_arg=data,
    )

    # run checks
    assert return_value is None

    assert state == [
        ('plugin-1', 'foo'),
        ('plugin-2', 'foo'),
    ]


def test_custom_return_values():
    from simple_plugin_manager.test_plugins import TestPlugin
    from simple_plugin_manager import PluginManager

    # setup plugins
    state = []
    data = 'foo'
    plugin_manager = PluginManager(hook_names=['handle_data'])

    plugin_manager.load([
        TestPlugin(name='plugin-1', state=state),
        TestPlugin(name='plugin-2', state=state, return_value='bar'),
        TestPlugin(name='plugin-3', state=state),
    ])

    # run hook 'handle_data'
    return_value = plugin_manager.run_hook_as_chain(
        hook_name='handle_data',
        hook_arg=data,
    )

    # run checks
    assert return_value is 'bar'

    assert state == [
        ('plugin-1', 'foo'),
        ('plugin-2', 'foo'),
    ]
