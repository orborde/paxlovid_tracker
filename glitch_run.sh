#!/bin/bash

source .env
./paxlovid_tracker.py \
    --webhook_url="$WEBHOOK_URL" \
    --coordinates="$COORDINATES"