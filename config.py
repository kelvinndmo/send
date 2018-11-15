import os


class Config:
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "CHANGE-TO-YOUR-LIKING******$%#%^******"


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
