try:
    import socketserver
    from app.controller import api
except ImportError as eImp:
    print(f"The following import error ocurred: {eImp}")

PORT = 5000 # Port to serve API

if __name__ == "__main__":
    try:
        Handler = api.MyHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Starting http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping by Ctrl+C")
        httpd.server_close()  # to solve problem "OSError: [Errno 98] Address already in use"
    except Exception as ex:
        print(f"The following error ocurred: {ex}")