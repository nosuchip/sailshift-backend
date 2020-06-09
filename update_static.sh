#!/bin/sh

rm -rf  backend/static/*
cp -r ../frontend/dist/* backend/static/
mv backend/static/static/* backend/static/
