#!/bin/zsh

# python3 scripts/download_bbox.py \
#     --token "MLY|9718956101555243|35209fada1e2d3a9a51754f657a3b0df" \
#     --bbox "90.428574,23.826125,90.429434,23.826193" \
#     --output "./downloads/300feet"

mapillary-download \
    --token "MLY|9718956101555243|35209fada1e2d3a9a51754f657a3b0df" \
    --bbox "90.420354,23.811901,90.424163,23.812734" \
    --output ./downloads/bragate