**nano /etc/systemd/system/test.service**
```
[Unit]
Description=tftp script
After=network.target
[Service]
User=a
Group=a
WorkingDirectory=/home/a/tftp
ExecStart=/home/a/tftp/venv/bin/python3 \
/home/a/tftp/tftp.py
[Install]
WantedBy=multi-user.target
```

```
systemctl daemon-reload
systemctl start test.service
systemctl enable test.service
```
