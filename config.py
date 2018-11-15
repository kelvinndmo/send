class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG=True
    TESTING=False

class TestingConfig(Config):
    DEBUG=True
    TESTING=True

class ProductionConfig(Config):
    pass


app_config={
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig,
    "default":DevelopmentConfig
}
