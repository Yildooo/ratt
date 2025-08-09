@echo off
title Hediye Kazanma Sistemi - Web Server
color 0A

echo.
echo ================================================
echo           HEDIYE KAZANMA SISTEMI
echo ================================================
echo.

REM Python kontrolü
echo Python kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Python bulunamadi!
    echo.
    echo Basit HTTP server baslatiliyor...
    echo.
    goto :simple_server
)

echo Python bulundu!
echo.
echo Web server baslatiliyor...
echo.

REM Python server'ı başlat
python basit_server.py
goto :end

:simple_server
echo.
echo ================================================
echo           BASIT HTTP SERVER
echo ================================================
echo.
echo Admin paneli: http://localhost:8080/istatistikler.html
echo Paylaşım linki: http://localhost:8080/hediye_kazanma.html
echo.
echo Tarayıcıda admin panelini açıyorum...
start http://localhost:8080/istatistikler.html
echo.
echo Server çalışıyor... (Kapatmak için bu pencereyi kapat)
python -m http.server 8080

:end
pause
