@echo off
echo Mencari Python dari instalasi Thonny...

set "P1=C:\Users\%USERNAME%\AppData\Local\Programs\Thonny\python.exe"
set "P2=C:\Program Files\Thonny\python.exe"
set "P3=C:\Program Files (x86)\Thonny\python.exe"
set "P4=C:\Thonny\python.exe"

if exist "%P1%" (
    echo Ditemukan di: %P1%
    "%P1%" main.py
    goto :eof
)

if exist "%P2%" (
    echo Ditemukan di: %P2%
    "%P2%" main.py
    goto :eof
)

if exist "%P3%" (
    echo Ditemukan di: %P3%
    "%P3%" main.py
    goto :eof
)

if exist "%P4%" (
    echo Ditemukan di: %P4%
    "%P4%" main.py
    goto :eof
)

echo.
echo [ERROR] Tidak dapat menemukan 'python.exe' dari Thonny secara otomatis.
echo.
echo Mohon jalankan program ini langsung dari dalam aplikasi Thonny,
echo ATAU edit file 'jalankan_disini.bat' ini dan masukkan path python.exe Anda.
echo.
pause
