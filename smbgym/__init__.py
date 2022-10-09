# from smbgym import Env
"""Registration code of Gym environments in this package."""
from .env import Env
# from .smb_random_stages_env import SuperMarioBrosRandomStagesEnv
from ._registration import make


# define the outward facing API of this package
__all__ = [
    make.__name__,
    Env.__name__,
    # SuperMarioBrosRandomStagesEnv.__name__,
]