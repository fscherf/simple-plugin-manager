Simple Plugin Manager
=====================

.. image:: https://img.shields.io/pypi/l/simple-plugin-manager.svg
    :alt: license MIT
    :target: https://pypi.org/project/simple-plugin-manager
.. image:: https://img.shields.io/pypi/pyversions/simple-plugin-manager.svg
    :alt: python 3
    :target: https://pypi.org/project/simple-plugin-manager
.. image:: https://img.shields.io/pypi/v/simple-plugin-manager.svg
    :alt: latest version
    :target: https://pypi.org/project/simple-plugin-manager
.. image:: https://github.com/fscherf/simple-plugin-manager/actions/workflows/ci.yml/badge.svg
    :alt: ci status
    :target: https://github.com/fscherf/simple-plugin-manager/actions/workflows/ci.yml
.. image:: https://img.shields.io/codecov/c/github/fscherf/simple-plugin-manager.svg
    :alt: code coverage
    :target: https://codecov.io/gh/fscherf/simple-plugin-manager/

*Simple Plugin Manager* is a simple plugin loading and management system, build
entirely on the Python standard library.

* `Installation <#installation>`_
* `Basic Usage <#basic-usage>`_


Installation
------------

.. code-block::

    pip install simple-plugin-manager


Basic Usage
-----------

.. code-block:: python

    from simple_plugin_manager import PluginManager

    # simple plugin with a hook that sets data['bar'] to 'bar'
    class Plugin:
        def handle_data(self, data):
            data['bar'] = 'bar'

    # setup plugin manager
    plugin_manager = PluginManager(hook_names=['handle_data'])

    plugin_manager.load([
        Plugin,
    ])

    # run plugin hook
    data = {'foo': 'foo'}

    plugin_manager.run_hook(
        hook_name='handle_data',
        hook_args=[data],
    )

    # finish
    assert data['foo'] == 'foo'
    assert data['bar'] == 'bar'

