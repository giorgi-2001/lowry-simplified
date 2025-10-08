#!/bin/bash

docker login

docker build -t giorgi023/lowry-backend:latest ./backend

docker push giorgi023/lowry-backend:latest

