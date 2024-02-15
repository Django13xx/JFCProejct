#!/bin/bash

# Get the directory of the script
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clear previous output files
> "$script_dir/aus/ausback/output_ausback.txt"
> "$script_dir/aus/ausfront/output_ausfront.txt"
> "$script_dir/Hardware/output_hardware.txt"

# Run command in ausback directory
cd "$script_dir/aus/ausback"
python manage.py runserver > "$script_dir/aus/ausback/output_ausback.txt" &

# Run command in ausfront directory
cd "$script_dir/aus/ausfront"
npm run dev > "$script_dir/aus/ausfront/output_ausfront.txt" &

# Run command in Hardware directory
cd "$script_dir/Hardware"
node app.js > "$script_dir/Hardware/output_hardware.txt" &

# Wait for python manage.py runserver to finish loading
while ! grep -q "Starting development server at http://127.0.0.1:8000/" "$script_dir/aus/ausback/output_ausback.txt"; do
    sleep 1
done

# Wait for npm run dev to finish loading
while ! grep -q "ausfront@0.0.0 dev" "$script_dir/aus/ausfront/output_ausfront.txt"; do
    sleep 1
done

# Clear output files
> "$script_dir/aus/ausback/output_ausback.txt"
> "$script_dir/aus/ausfront/output_ausfront.txt"
> "$script_dir/Hardware/output_hardware.txt"

# Open the specified URL in the default browser
open "http://localhost:5173/"