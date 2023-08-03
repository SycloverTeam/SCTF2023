#!/bin/bash

echo $FLAG > /flag
service nginx start
redis-server /etc/redis/redis.conf &
node /app/server/server.js