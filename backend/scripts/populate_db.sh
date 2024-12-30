#!/bin/bash

poetry run alembic downgrade base

poetry run alembic upgrade head


echo "Running create_superuser.py..."
poetry run python src/utils/create_superuser.py

if [ $? -eq 0 ]; then
    echo "Successfully ran create_superuser.py."
else
    echo "Error running create_superuser.py. Exiting."
    exit 1
fi

echo "Running populate_table.py..."
 poetry run python src/utils/populate_table.py

if [ $? -eq 0 ]; then
    echo "Successfully ran sync_stripe_db.py."
else
    echo "Error running sync_stripe_db.py. Exiting."
    exit 1
fi

echo "Both scripts executed successfully."