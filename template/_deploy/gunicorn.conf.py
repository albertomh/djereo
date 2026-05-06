# ruff: noqa: INP001, S108

import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
accesslog = "-"
errorlog = "-"
worker_tmp_dir = "/dev/shm"
