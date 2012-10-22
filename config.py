
class Config(object):
	DEBUG = False

class ProductionConfig(Config):
	DATA_SOURCE = 'mongo'

class DevelopmentConfig(Config):
	DEBUG = True
