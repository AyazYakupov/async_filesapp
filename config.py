import sys


class CONFIG:
    HOST = '0.0.0.0'
    PORT = 5000
    FILES_DIR = 'files_app/files/'

    DB_NAME = 'files.db'
    DB_CONFIG = 'sqlite:///{}'.format(DB_NAME)
    LOGGING = dict(
        version=1,
        disable_existing_loggers=False,
        loggers={
            "sanic.root": {"level": "INFO", "handlers": ["internal", "internalFile"]},
            "sanic.error": {
                "level": "INFO",
                "handlers": ["errorStream", "errorFile"],
                "propagate": True,
                "qualname": "sanic.error",
            },
            "sanic.access": {
                "level": "INFO",
                "handlers": ["accessStream", "accessFile"],
                "propagate": True,
                "qualname": "sanic.access",
            },
        },
        formatters={
            'simple': {
                'format': '%(asctime)s - (%(name)s)[%(levelname)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'access': {
                'format': '%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: ' +
                          '%(request)s %(message)s %(status)d %(byte)d',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        handlers={
            'internalFile': {
                'class': 'logging.FileHandler',
                'formatter': 'simple',
                'filename': "temp/clickinternal.log"
            },
            'accessFile': {
                'class': 'logging.FileHandler',
                'formatter': 'access',
                'filename': "temp/clickaccess.log"
            },
            'errorFile': {
                'class': 'logging.FileHandler',
                'formatter': 'simple',
                'filename': "temp/clickerr.log"
            },
            'internal': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': sys.stderr
            },
            'accessStream': {
                'class': 'logging.StreamHandler',
                'formatter': 'access',
                'stream': sys.stderr
            },
            'errorStream': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': sys.stderr
            }
        },
    )

    def get_db_config(self):
        return self.DB_CONFIG

    def get_db_name(self):
        return self.DB_NAME

    def get_files_dir(self):
        return self.FILES_DIR

    def get_log_config(self):
        return self.LOGGING

    def get_host(self):
        return self.HOST

    def get_port(self):
        return self.PORT
