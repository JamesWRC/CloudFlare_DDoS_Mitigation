#!/bin/bash

#   Start the 'runner' in the background which will periodicly get retrieve the latest Cloudflare logs and parse them.
/codebase/runner.sh &

#   Start the Flask server.
/codebase/app.py