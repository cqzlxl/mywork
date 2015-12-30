##-*-coding: utf-8;-*-##
import os.path
import sys
import logging


logger = logging.getLogger(__name__)

loaded_modules = dict()

reload_exclude = {
    __name__,
    'logging',
    'os',
    'os.path',
    'sys'
}


def do_reload():
    for name in sys.modules:
        logger.debug('try to reload module: %s', name)

        if name in sys.builtin_module_names:
            logger.debug('not reloaded, builtin')
            continue

        if name in reload_exclude:
            logger.debug('not reloaded, excluded')
            continue

        module = sys.modules[name]
        filename = getattr(module, '__file__', None)
        if filename is None or not os.path.isfile(filename):
            logger.debug('not reloaded, module file not found: %s', filename)
            continue
        if filename[-4:] in ('.pyc', '.pyd', '.pyo'):
            filename = filename[:-1]

        try:
            newtime = os.stat(filename).st_mtime
        except Exception:
            logger.exception('not reloaded, can not stat module file: %s', filename)
            continue

        oldtime = loaded_modules.get(name)
        if oldtime is None:
            loaded_modules[name] = newtime
            logger.debug('not reloaded, not modified recently')
            continue

        if oldtime >= newtime:
            logger.debug('not reloaded, not modified recently')
            continue

        reload(module)

        loaded_modules[name] = newtime
        logger.info('reloaded module %s', name)
