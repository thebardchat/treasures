import http.server
import socketserver
import os

PORT = 8080  # Changed from 8000
DIRECTORY = r"A:\Angel_Cloud"

os.chdir(DIRECTORY)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"--- FILE SERVER ACTIVE ---")
    print(f"Serving: {DIRECTORY}")
    print(f"Access at: http://192.168.1.100:{PORT}")
    print("Press CTRL+C to stop")
    httpd.serve_forever()