#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

export FLASK_APP=server:app

if [ ! -d "migrations" ]; then
    flask db init
fi

flask db migrate -m "Auto migration"
flask db upgrade
