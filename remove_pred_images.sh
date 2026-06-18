#!/bin/bash

# Remove all image files ending with "_pred" from './demo_images copy'

echo "Removing files matching '_pred' pattern..."

ls './demo_images copy' | grep "_pred" | while read file; do
    filepath="./demo_images copy/$file"
    if [ -f "$filepath" ]; then
        rm "$filepath"
        echo "Removed: $file"
    fi
done

echo "Done!"
