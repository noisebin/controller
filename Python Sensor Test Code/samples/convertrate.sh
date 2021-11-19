#!/bin/bash
for i in *.wav; do ffmpeg -i "$i" -ar 48000 "${i%.*}2.wav"; done
