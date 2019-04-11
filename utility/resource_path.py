import sys
import os


def resource_path(relative):
    """
    Помошник для поиска путей файлов.
    После помпиляции программы в .exe , ресурсные файлы хранятся ов временной папке.
    Для того, чтобы использовать одни пути при разработке и при запуске программы в .exe используется эта функция.
    Например, для подключения файла 'utility/qtbase_ru.qm' используйте:
        filename = resource_path('utility/qtbase_ru.qm')
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)
