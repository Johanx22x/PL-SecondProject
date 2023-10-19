from swiplserver import PrologMQI, PrologThread


class Singleton(type):
    """Singleton metaclass."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return the same instance of the class."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Prolog(metaclass=Singleton):
    """Prolog class."""
    def __init__(self):
        """Initialize the Prolog class."""
        self.mqi = PrologMQI()
        self.prolog_thread = self.mqi.create_thread()

        # Set encoding
        self.prolog_thread.query("set_prolog_flag(encoding,utf8).")

    def query(self, query_str):
        """Query the Prolog knowledge base."""
        result = self.prolog_thread.query(query_str)
        return result

    def reset(self):
        """Reset the Prolog knowledge base."""
        # Close the existing PrologThread to reset the knowledge
        self.prolog_thread.close()

        # Create a new PrologThread with a fresh knowledge base
        self.prolog_thread = self.mqi.create_thread()

    def close(self):
        """Close the Prolog connection."""
        # Close the PrologThread and release resources
        self.prolog_thread.close()
