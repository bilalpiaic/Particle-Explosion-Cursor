"""Production-ready Gunicorn configuration."""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = max(1, (multiprocessing.cpu_count() * 2) + 1)
worker_class = "gthread"
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Restart workers after this many requests, with some randomness
worker_tmp_dir = "/dev/shm"  # Use RAM for temporary files

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info" if os.environ.get('FLASK_ENV') == 'production' else "debug"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
forwarded_allow_ips = "*"
proxy_allow_from = "*"

# Process naming
proc_name = "interactive-particle-system"

# Preload application for better memory usage
def when_ready(server):
    server.log.info("Interactive Particle System ready for production")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")