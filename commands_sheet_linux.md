# Linux Commands Cheat Sheet

## Navigation
pwd                          # show current directory
ls -la                       # list all files with permissions
cd ~/devops/week5            # go to directory
cd ..                        # go up one level
mkdir -p ~/devops/week8      # create nested folders

## File Operations
touch file.txt               # create empty file
cat file.txt                 # print file contents
cp file.txt backup.txt       # copy file
mv old.txt new.txt           # rename/move file
rm -r foldername             # delete folder and contents (NO UNDO)
echo "text" > file.txt       # write text to file (overwrites)
echo "text" >> file.txt      # append text to file

## Permissions
ls -l                        # view permissions
chmod 755 script.sh          # rwx r-x r-x
chmod 644 file.txt           # rw- r-- r--
chmod 600 secret.txt         # rw- --- ---
chmod 400 key.pem            # r-- --- --- (SSH key)
chmod u+x script.sh          # add execute for owner

## Processes
ps aux                       # list all running processes
ps aux | grep python         # find python processes
kill 1234                    # stop process with PID 1234
kill -9 1234                 # force kill process
killall python3              # kill all python3 processes
top                          # live process viewer (q to quit)
jobs                         # list background jobs

## Running in Background
python3 app.py &                          # run in background
nohup python3 app.py > app.log 2>&1 &     # survives terminal close
kill $(ps aux | grep 'python3 app.py' | grep -v grep | awk '{print $2}')

## Networking
ip addr show | grep 'inet '  # find your IP address
ping -c 4 google.com         # test connectivity
ss -tulnp                    # show all open ports
ss -tulnp | grep :5000       # check if port 5000 is open
curl http://localhost:5000/api/health     # test Flask endpoint
dig +short github.com        # DNS lookup

## Logs
sudo tail -f /var/log/syslog             # watch system log live
tail -f app.log                          # watch app log live
grep -i 'error' app.log                  # search for errors
grep '404' flask_production.log          # find 404 errors
sudo journalctl -u flaskapp -f           # systemd service logs

## System Resources
df -h                        # disk usage
free -h                      # memory usage
uptime                       # system load average

## systemd Service
sudo nano /etc/systemd/system/flaskapp.service
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl stop flaskapp
sudo systemctl enable flaskapp
sudo systemctl status flaskapp
sudo journalctl -u flaskapp --since '5 min ago'
