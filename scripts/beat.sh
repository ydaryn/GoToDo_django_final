#!/bin/sh

celery -A settings beat -l info
