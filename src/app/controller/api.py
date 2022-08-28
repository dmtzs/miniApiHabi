
try:
    import json
    import http.server
    from .auth import Authorization
except ImportError as eImp:
    print(f"The following import error ocurred in {__file__}: {eImp}")

class MyHandler(http.server.SimpleHTTPRequestHandler, Authorization):
    def error_response(self, message, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        output_data = {
            "status": "Error",
            "message": message
        }
        output_json = json.dumps(output_data)
        
        self.wfile.write(output_json.encode('utf-8'))

    def success_response(self, body):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        output_json = json.dumps(body)
        
        self.wfile.write(output_json.encode("utf-8"))

    def do_GET(self): # The name of the function doesnt follow the snake case but built in library needs the name of the function like this
        # authorization
        username, passwd = self.dec_basic_auth(self.headers["Authorization"])
        if username == "error_username" or passwd == "error_passwd":
            self.error_response("Unauthorized", 401)

        else:
            username_db, passwd_db = self.get_username_passwd_db(username)
            if username_db == "error_username" or passwd_db == "error_passwd":
                self.error_response("Unauthorized", 401)

            else:
                if username == username_db and passwd == passwd_db:
                    endpoint_params = self.path.split("?")
                    endpoint = endpoint_params[0]

                    if endpoint == "/properties":
                        if len(endpoint_params) < 2:
                            params = {}
                        else:
                            params = endpoint_params[1]

                            if "&" not in params:
                                params = params.split("=")
                                params = {
                                    params[0]: params[1]
                                }

                            elif "&" in params:
                                all_params = params.split("&")
                                params = {}
                                for single_param in all_params:
                                    key, value = single_param.split("=")
                                    params[key] = value

                            else:
                                self.error_response("Bad request", 400)

                        properties = self.get_properties(params)
                        if len(properties) == 0:
                            self.error_response("No records found", 404)

                        else:
                            output_data = {
                                "status": "success",
                                "properties": properties
                            }
                            self.success_response(output_data)

                    else:
                        self.error_response("Bad request, verify called endpoint", 400)
                else:
                    self.error_response("Unauthorized", 401)