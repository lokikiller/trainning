import os

def env_default(k, default):
    v = os.environ.get(k, default)
    globals()[k] = v

env_default("APP_HOST", '0.0.0.0')
env_default("APP_PORT", 8081)

env_default("DEBUG",  True)
