import http.server
import socketserver
import socket

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/hediye_kazanma.html'
        return super().do_GET()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    ip = get_ip()
    print("=" * 50)
    print("🎁 HEDİYE KAZANMA SİSTEMİ BAŞLADI!")
    print("=" * 50)
    print(f"📱 Paylaşım Linki: http://{ip}:{PORT}")
    print(f"📊 Admin Panel: http://localhost:{PORT}/istatistikler.html")
    print("=" * 50)
    print("✅ Server çalışıyor... (Ctrl+C ile durdur)")
    httpd.serve_forever()
