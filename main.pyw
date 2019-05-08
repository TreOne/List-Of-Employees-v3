import logging
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator
from utility.resource_path import resource_path
from utility.settings import Settings
from view.mw_view import MWView


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def prepare_app(app_var):
    app_settings = Settings()

    # Внешний вид приложения
    theme_style = app_settings.get('appearance', 'theme_style')  # default/fusion
    if theme_style == 'fusion':
        app_var.setStyle('Fusion')

    # Руссификация интерфейса QT
    translator = QTranslator(app_var)
    translator.load(resource_path('resources/qtbase_ru.qm'))
    app_var.installTranslator(translator)


def start_logging():
    # Логирование ошибок
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)-8s:%(name)s:%(message)s',
        filename=os.path.join(os.getenv('APPDATA'), 'el_log.log'),
        filemode='a'
    )
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s:%(levelname)-8s:%(name)s:%(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl


if __name__ == '__main__':
    if len(sys.argv) > 1:
        param_name = sys.argv[1]
        if param_name == "-d":
            start_logging()

    # Запуск основного потока
    app = QtWidgets.QApplication(sys.argv)
    prepare_app(app)
    main_window = MWView()
    sys.exit(app.exec_())
