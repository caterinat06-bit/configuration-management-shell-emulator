@echo off
echo --- Running test with custom prompt ---
python main.py --prompt "MyShell> "

echo.
echo --- Running test with startup script ---
python main.py --script startup.txt

echo.
echo --- Running test with all parameters ---
python main.py --vfs my_vfs.csv --prompt "TestVFS # " --script startup.txt

echo
echo "--- Running full VFS test ---"
python3 main.py --vfs my_vfs.csv --script vfs_test_script.txt

pause