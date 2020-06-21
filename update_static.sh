#!/bin/sh

rm -rf  backend/static/*
cp -r ../frontend/dist/* backend/static/
mv backend/static/static/* backend/static/
sed -i 's/\/img\//\/static\/img\//g' backend/static/index.html
sed -i 's/\/img\//\/static\/img\//g' backend/static/manifest.json
