#!/bin/zsh

# python3 scripts/download_bbox.py \
#     --token "MLY|9718956101555243|35209fada1e2d3a9a51754f657a3b0df" \
#     --bbox "90.428574,23.826125,90.429434,23.826193" \
#     --output "./downloads/300feet"

# Dhaka metropolitan area
# 23.898309, 90.330569 Ashulia
# 23.661048, 90.509149 Narayanganj

mapillary-download \
    --token "MLY|9718956101555243|35209fada1e2d3a9a51754f657a3b0df" \
    --username "sawanshariar" \
    --bbox "90.330569,23.661048,90.509149,23.898309" \
    --output ./downloads/bragate