# -*- coding: utf-8 -*-

def classFactory(iface):
    """Factory called when plugin is loaded to create the plugin instance."""
    from .plugin import PreValCarPlugin
    return PreValCarPlugin(iface)
