def test_basic_execution():
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
        TestPlugin(name='Plugin-4', state=state, raise_runtime_error=True)
    ])

    # run hook 'handle_data'
    return_values = plugin_manager.run_hook(
        hook_name='handle_data',
        hook_args=[data],
    )

    # run checks
    assert plugin_manager.get_hook_names() == ['handle_data']
    assert len(return_values) == 4

    assert return_values[0] == 'foo'
    assert return_values[1] == 'foo'
    assert return_values[2] == 'foo'
    assert isinstance(return_values[3], RuntimeError)

    assert state == [
        ('plugin-1', 'foo'),
        ('plugin-2', 'foo'),
        ('plugin-3', 'foo'),
    ]
