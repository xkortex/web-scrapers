import os
from core.config import loader


def bootstrap():
    """Ensures the environment is set up properly, sets Keras backend"""
    backend = loader.get_cfg_param('global', 'backend')
    os.environ['KERAS_BACKEND'] = backend
    import keras
    print('Keras v', keras.__version__)


if __name__ == '__main__':
    bootstrap()