class Singleton(type):
    _instalce = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instalce:
            cls._instalce[cls] = super().__call__(*args, **kwargs)

        return cls._instalce[cls]