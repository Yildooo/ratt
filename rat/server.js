const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = 8080;

// MIME types
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml',
};

// Get local IP
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const interface of interfaces[name]) {
            if (interface.family === 'IPv4' && !interface.internal) {
                return interface.address;
            }
        }
    }
    return 'localhost';
}

// Create server
const server = http.createServer((req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    let filePath = req.url === '/' ? '/hediye_kazanma.html' : req.url;
    filePath = path.join(__dirname, filePath);

    // Check if file exists
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            res.writeHead(404);
            res.end('404 - File Not Found');
            return;
        }

        // Get file extension
        const extname = path.extname(filePath).toLowerCase();
        const contentType = mimeTypes[extname] || 'application/octet-stream';

        // Read and serve file
        fs.readFile(filePath, (err, content) => {
            if (err) {
                res.writeHead(500);
                res.end('500 - Internal Server Error');
                return;
            }

            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        });
    });
});

// Start server
server.listen(PORT, () => {
    const localIP = getLocalIP();
    
    console.log('='.repeat(60));
    console.log('🎁 HEDİYE KAZANMA SİSTEMİ BAŞLADI!');
    console.log('='.repeat(60));
    console.log(`📱 Paylaşım Linki: http://${localIP}:${PORT}`);
    console.log(`📊 Admin Panel: http://localhost:${PORT}/istatistikler.html`);
    console.log(`🎁 Hediye Link: http://${localIP}:${PORT}/hediye_kazanma.html`);
    console.log('='.repeat(60));
    console.log('📋 KULLANIM:');
    console.log('1. Paylaşım linkini kopyala');
    console.log('2. WhatsApp/Telegram\'da paylaş');
    console.log('3. Admin panel ile kontrol et');
    console.log('4. Ctrl+C ile durdur');
    console.log('='.repeat(60));
    console.log('✅ Server çalışıyor...');
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n🛑 Server durduruldu.');
    process.exit(0);
});
