#!/bin/bash

 python index.py --host 0.0.0.0 --port 8050 --debug

# if [ "$DEBUG" = "true"  ]; then
   
# else
#     gunicorn index:server -b :8050 -w 12
#  fi
