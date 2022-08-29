try:
    import pymysql
    from app import logger, db_credentials
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

class MySql():
    def db_connection(self):
        try:
            connection = pymysql.connect(host=db_credentials["host"],
                                            port=db_credentials["port"],
                                            user=db_credentials["username"],
                                            password=db_credentials["passwd"],
                                            database=db_credentials["db_name"],
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
                    sql = """
                    SELECT address, city, price, description, status FROM 
                    (SELECT Pty.address, Pty.city, Pty.price, Pty.description, Pty.year, S.name AS status
                    FROM property Pty
                    LEFT JOIN status_history SH ON Pty.id=SH.property_id
                    LEFT JOIN status S ON SH.status_id=S.id
                    WHERE (S.name='pre_venta' OR S.name='vendido' OR S.name='en_venta')) res 
                    """

                    keys = list(params.keys())
                    if len(keys) != 0:
                        sql += "WHERE "

                        for index, key in enumerate(keys):
                            my_filter = f"{key}='{params[key]}'"
                            if len(keys) > 1 and index < len(keys)-1:
                                sql += my_filter + " AND "
                            else:
                                sql += my_filter
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) == 0:
                        raise Exception("Could not found any record")

                    return result
        except Exception as ex:
            logger.error("Failed retrieving properties", extra={"error": f"{ex}"})
            return []