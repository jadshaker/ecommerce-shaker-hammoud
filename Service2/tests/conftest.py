def pytest_configure():
    """
    This function is a pytest hook that is called to configure the pytest environment.
    It performs the following actions:
    1. Imports the `os` and `sys` modules.
    2. Determines the top-level directory of the project by navigating one level up from the directory of this file.
    3. Appends the top-level directory to the system path (`sys.path`), allowing for the import of modules from the top-level directory during testing.
    """
    import os
    import sys

    topdir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(topdir)
