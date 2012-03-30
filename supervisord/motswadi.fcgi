[program:motswadi.fcgi]
command=/var/praekelt/motswadi/motswadi/manage.py runfcgi host=127.0.0.1 port=8102 protocol=fcgi daemonize=False method=threaded
user=ubuntu
stdout_logfile=/var/praekelt/motswadi/logs/fcgi.log
redirect_stderr=true
stopsignal=QUIT
environment=PYTHON_EGG_CACHE='/var/www/.python-eggs'
