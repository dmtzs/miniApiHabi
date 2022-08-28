try:
    import logging
    import ecs_logging
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.json')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)