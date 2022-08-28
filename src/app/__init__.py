try:
    import toml
    import base64
    import logging
    import ecs_logging
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

# -------------------------Creating logger to do logs-------------------------
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.json')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

# -------------------------Upload credentials from file-------------------------
with open("credentials.toml", "r", encoding="utf8") as tomlFile:
    db_credentials = toml.load(tomlFile)

    for decoded_cred in db_credentials["database"]:
        bytes_object = db_credentials["database"][decoded_cred].encode("utf8")
        base64_bytes = base64.b64decode(bytes_object)
        db_credentials["database"][decoded_cred] = base64_bytes.decode("utf8")
    db_credentials = db_credentials["database"]
    db_credentials["port"] = int(db_credentials["port"])