import http.server
import json
import sqlite3
import uuid
import time

# In-memory token storage (simple)
tokens = {}

# Initialize database tables if they don't exist
conn = sqlite3.connect('app.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS posts 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT)''')
conn.commit()
conn.close()

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect to login page
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
        elif self.path == '/login':
            # Serve the login HTML
            try:
                with open('login.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Login page not found')
        elif self.path == '/register':
            # Serve the register HTML
            try:
                with open('register.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Register page not found')
        elif self.path == '/posts':
            # Serve the posts HTML
            try:
                with open('posts.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Posts page not found')
        elif self.path == '/api/posts':
            # Get all posts (public)
            conn = sqlite3.connect('app.db')
            c = conn.cursor()
            c.execute("SELECT username, message FROM posts")
            posts = [{"user": row[0], "msg": row[1]} for row in c.fetchall()]
            conn.close()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        if self.path == '/register':
            if 'username' in data and 'password' in data:
                username = data['username']
                password = data['password']
                conn = sqlite3.connect('app.db')
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(b'{"message": "Registered"}')
                except sqlite3.IntegrityError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Username exists"}')
                finally:
                    conn.close()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing fields"}')

        elif self.path == '/login':
            if 'username' in data and 'password' in data:
                username = data['username']
                password = data['password']
                conn = sqlite3.connect('app.db')
                c = conn.cursor()
                c.execute("SELECT password FROM users WHERE username=?", (username,))
                row = c.fetchone()
                conn.close()
                if row and row[0] == password:
                    token = str(uuid.uuid4())
                    tokens[token] = username
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({"token": token}).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Invalid credentials"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing fields"}')

        elif self.path == '/post':
            auth = self.headers.get('Authorization')
            if not auth or auth not in tokens:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "Unauthorized"}')
                return
            if 'message' in data:
                username = tokens[auth]
                message = data['message']
                # Simulate background task (pretend waiting/processing)
                time.sleep(2)
                conn = sqlite3.connect('app.db')
                c = conn.cursor()
                c.execute("INSERT INTO posts (username, message) VALUES (?, ?)", (username, message))
                conn.commit()
                conn.close()
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b'{"message": "Posted"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing message"}')

        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Starting server on http://localhost:8000')
    httpd.serve_forever()