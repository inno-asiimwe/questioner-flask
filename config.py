"""Module contains configurations for the app"""
import os


class Config:
    """The Parent configurations for the app"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_TIME = 31536000
    BUNDLE_ERRORS = True


class DevelopmentConfig(Config):
    """Class for development configurations"""
    DEBUG = True


class TestingConfig(Config):
    """Class for the testing configurations"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    TOKEN_TIME = 2


class StagingConfig(Config):
    """Class for the staging configurations"""
    DEBUG = True


class ProductionConfig(Config):
    """Class for the Production configurations"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
