set shell := ["bash", "-cu"]

default:
    just --list

install:
    pipx install --editable .

reinstall:
    pipx reinstall --editable .

test:
    python -m py_compile lightctl.py lightctl/*.py

list:
    lightctl list

status device:
    lightctl status {{device}}

on device:
    lightctl on {{device}}

off device:
    lightctl off {{device}}
