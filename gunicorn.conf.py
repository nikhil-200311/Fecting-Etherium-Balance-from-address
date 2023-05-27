import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "-"

accesslog = "-"
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

preload_app = True
daemon = True
module_name = "piyush.wsgi"
