import logging
import time
from functools import wraps


def retry(exceptions=None, tries=3, delay=5, backoff=2, logger=logging.getLogger(__name__),
          infinite_retry_exceptions=None):
    """
    Повторяет выполнение функции в случае возникновения исключений.

    Args:
        exceptions: Исключение или кортеж исключений, при которых повтор НЕ будет выполняться.
                      Если None, повтор будет выполняться при любых исключениях.
        tries: Максимальное количество попыток выполнения функции (по умолчанию 3).
        delay: Начальная задержка перед повтором (в секундах, по умолчанию 1).
        backoff: Множитель увеличения задержки после каждой неудачной попытки (по умолчанию 2).
        logger: Объект логгера для вывода информации о повторах.
        infinite_retry_exceptions: Исключение или кортеж исключений, при которых
                                     повтор будет выполняться бесконечно.
    """
    if infinite_retry_exceptions is None:
        infinite_retry_exceptions = tuple()
    if exceptions is None:
        exceptions = tuple()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _delay = delay
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    raise
                except infinite_retry_exceptions as e:
                    logger.warning(f"Function '{func.__name__}' failed with error: {e}. Infinite Retrying...")
                    time.sleep(delay)
                except Exception as e:
                    if attempt >= tries:
                        raise
                    logger.warning(f"Function '{func.__name__}' failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(_delay)
                    _delay *= backoff
                    attempt += 1

        return wrapper

    return decorator