#!/bin/sh
celery -A settings worker -l info
