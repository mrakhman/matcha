import multiprocessing

app_name = "matcha.api"
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

loglevel = 'info'
reload = False
timeout = 90
