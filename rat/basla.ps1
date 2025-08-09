# PowerShell HTTP Server
$port = 8080
$url = "http://localhost:$port/"

# Get local IP
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.InterfaceAlias -notlike "*Teredo*"} | Select-Object -First 1).IPAddress

Write-Host "=" * 60 -ForegroundColor Green
Write-Host "🎁 HEDİYE KAZANMA SİSTEMİ BAŞLADI!" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "📱 Paylaşım Linki: http://$localIP`:$port" -ForegroundColor Cyan
Write-Host "📊 Admin Panel: http://localhost:$port/istatistikler.html" -ForegroundColor Cyan
Write-Host "🎁 Hediye Link: http://$localIP`:$port/hediye_kazanma.html" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "📋 KULLANIM:" -ForegroundColor White
Write-Host "1. Paylaşım linkini kopyala" -ForegroundColor White
Write-Host "2. WhatsApp/Telegram'da paylaş" -ForegroundColor White
Write-Host "3. Admin panel ile kontrol et" -ForegroundColor White
Write-Host "4. Ctrl+C ile durdur" -ForegroundColor White
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ Server çalışıyor..." -ForegroundColor Green

# Start HTTP listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

# Open admin panel in browser
Start-Process "http://localhost:$port/istatistikler.html"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Get requested file
        $requestedFile = $request.Url.LocalPath
        if ($requestedFile -eq "/") {
            $requestedFile = "/hediye_kazanma.html"
        }
        
        $filePath = Join-Path $PSScriptRoot $requestedFile.TrimStart('/')
        
        # Log visitor
        $clientIP = $request.RemoteEndPoint.Address
        $userAgent = $request.UserAgent
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        Write-Host "📝 Ziyaretçi: $clientIP - $timestamp - $requestedFile" -ForegroundColor Yellow
        
        # Serve file
        if (Test-Path $filePath) {
            $content = Get-Content $filePath -Raw -Encoding UTF8
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            
            $response.ContentType = "text/html; charset=utf-8"
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        } else {
            $response.StatusCode = 404
            $errorContent = "404 - File Not Found"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorContent)
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }
        
        $response.Close()
    }
} finally {
    $listener.Stop()
    Write-Host "🛑 Server durduruldu." -ForegroundColor Red
}
