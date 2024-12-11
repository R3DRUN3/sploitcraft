from http.server import SimpleHTTPRequestHandler, HTTPServer

class MaliciousHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Captured request: {self.path}")
        # Log query parameters
        if '?' in self.path:
            query = self.path.split('?')[1]
            print(f"Captured query: {query}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Malicious server: Data captured successfully!")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MaliciousHandler)
    print("Malicious server running on http://localhost:8000")
    server.serve_forever()
