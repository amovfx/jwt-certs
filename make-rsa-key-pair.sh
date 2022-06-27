#!/bin/bash
mkdir -p ./keys
openssl genrsa -out ./keys/key.pem 2048
openssl rsa -in ./keys/key.pem -outform PEM -pubout -out ./keys/public.pem