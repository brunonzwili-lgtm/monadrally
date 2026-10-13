#!/usr/bin/env python3
"""Upload a staged Sol Rally static site to Vercel production.

Run detached (double-fork + setsid) because the ~100MB upload outlives any
shell timeout, mirroring what serve.py does for the dev server.

Usage: deploy_vercel.py [stage-dir] [log-path] [vercel-project-name]
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STAGE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "deploy")
LOG = sys.argv[2] if len(sys.argv) > 2 else "/tmp/vercel_deploy.log"
PROJECT = sys.argv[3] if len(sys.argv) > 3 else None

if os.fork() > 0:
    os._exit(0)

os.setsid()

if os.fork() > 0:
    os._exit(0)

os.chdir(STAGE)
log = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.dup2(log, 1)
os.dup2(log, 2)
devnull = os.open(os.devnull, os.O_RDONLY)
os.dup2(devnull, 0)

argv = ["vercel", "deploy", "--prod", "--yes", "--archive=tgz"]
if PROJECT:
    argv += ["--name", PROJECT]

os.execvp("vercel", argv)