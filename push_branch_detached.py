#!/usr/bin/env python3
"""Push a branch to GitHub detached so a large repo transfer outlives the shell."""
import os
import sys

REPO = "/Users/h/Documents/stk-code-wasm"
LOG = "/tmp/push_monad.log"
REMOTE = sys.argv[1] if len(sys.argv) > 1 else "monadrally"
BRANCH = sys.argv[2] if len(sys.argv) > 2 else "monad"
REPO = sys.argv[3] if len(sys.argv) > 3 else REPO

if os.fork() > 0:
    os._exit(0)
os.setsid()
if os.fork() > 0:
    os._exit(0)

os.chdir(REPO)
log = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.dup2(log, 1)
os.dup2(log, 2)
devnull = os.open(os.devnull, os.O_RDONLY)
os.dup2(devnull, 0)

os.execvp("git", ["git", "push", "-u", REMOTE, BRANCH])