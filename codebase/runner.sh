#!/bin/bash

#   Running this every 5 seconds will cost you ~300 out of your 1200 API requests per 5 minutes.
#   Lets say worst case you take action on 4 IP's / hosts every 5 seconds this tool will cost a max of 
while true; do
  python3 /codebase/log2action.py
  sleep 5;
done