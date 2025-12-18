
import unittest
import importlib


class TestPackage(unittest.TestCase):
    def test_import_pkg(self):
        """Test that the package can be imported."""
        try:
            import AIFoundationKit
        except ImportError as e:
            self.fail(f"Failed to import AIFoundationKit: {e}")

    def test_import_submodules(self):
        """Test importing submodules to ensure structure is intact."""
        submodules = [
            'AIFoundationKit.base',
            'AIFoundationKit.rag',
            'AIFoundationKit.genai'
        ]
        for module in submodules:
            try:
                importlib.import_module(module)
            except ImportError as e:
                self.fail(f"Failed to import submodule {module}: {e}")


if __name__ == '__main__':
    unittest.main()
