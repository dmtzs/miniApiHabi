try:
    import pymysql
    from app import logger
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

class MySql():
    db_credentials = {
        "username": "pruebas",
        "passwd": "VGbt3Day5R",
        "dbName": "habi_db",
        "port": 3309,
        "host": "3.130.126.210"
        }

    def db_connection(self):
        try:
            connection = pymysql.connect(host=self.db_credentials["host"],
                                            port=self.db_credentials["port"],
                                            user=self.db_credentials["username"],
                                            password=self.db_credentials["passwd"],
                                            database=self.db_credentials["dbName"],
                                            cursorclass=pymysql.cursors.DictCursor)
            logger.info("Username and password successfully decoded from basic auth")
            return connection
        except Exception as ex:
            logger.error("Failed doing the connection to db", extra={"error": f"{ex}"})
            return "connection_error"
    
    def get_properties(self, params):
        try:
            logger.info("Creating db connection to get properties")
            connection = self.db_connection()
            if type(connection).__name__ == "str":
                raise Exception("Error in trying to use connection to database")
        except Exception as ex:
            logger.error("Failed to create the db connection", extra={"error": f"{ex}"})
            return []
        
        try:
            with connection:
                with connection.cursor() as cursor:
                    sql = ""
                    if len(params) == 1:
                        sql = "SELECT address, city, username FROM auth_user WHERE username=eder"
                    else:
                        # Hacer algo aquí en caso de que se reciban más de un param
                        pass
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) == 0:
                        raise Exception("Could not found any record")

                    return result
        except Exception as ex:
            logger.error("Failed retrieving properties", extra={"error": f"{ex}"})
            return []