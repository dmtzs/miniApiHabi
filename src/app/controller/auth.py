try:
    import base64
    from ..queries.database import MySql
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

class Authorization(MySql):
    def dec_basic_auth(self, auth_header) -> str:
        try:
            only_creds = auth_header.split(" ")
            base64_bytes = only_creds[1].encode("ascii")
            messsage_bytes = base64.b64decode(base64_bytes)
            decoded_creds = messsage_bytes.decode("ascii")
            username, passwd = decoded_creds.split(":")

            return username, passwd
        except Exception as ex:
            # error_payload = {
            #     "errorDesc": "Error trying to decode basic auth credentials",
            #     "errorTraceback": f"{ex}"
            # }
            return "error_username", "error_passwd"
    
    def get_username_passwd_db(self, main_user) -> str:
        try:
            connection = self.db_connection()
            if type(connection).__name__ == "str":
                return "error_username", "error_passwd"
        except Exception as ex:
            # error_payload = {
            #     "errorDesc": "Error trying to connect to database",
            #     "errorTraceback": f"{ex}"
            # }
            return "error_username", "error_passwd"
        
        try:
            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT id, password, username FROM auth_user WHERE username=%s"
                    cursor.execute(sql, (main_user,))
                    result = cursor.fetchone()
                    if result is None:
                        raise Exception("Could not found any record")

                    return result["username"], result["password"]
        except Exception as ex:
            # error_payload = {
            #     "errorDesc": "Error trying to execute the query",
            #     "errorTraceback": f"{ex}"
            # }
            return "error_username", "error_passwd"