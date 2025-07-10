import globalPluginHandler
import ui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()

    def script_testMessage(self, gesture):
        """Test if the add-on is working."""
        ui.message("Papa Voice Minimal is working! Add-on loaded successfully.")
    
    script_testMessage.__doc__ = "Test if Papa Voice Minimal add-on is working"
    
    # Simple gesture for testing
    __gestures = {
        "kb:nvda+shift+t": "testMessage",
    } 