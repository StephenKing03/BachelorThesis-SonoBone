# globals.py
class GlobalState:
    _instance = None
    exit_program = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalState, cls).__new__(cls, *args, **kwargs)
        return cls._instance