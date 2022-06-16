
Development setup
-----------------

Create virtualenv

    cd /var/envs && mkvirtualenv --python=<python_path> currency_exchange


Install requirements for a project.

    cd /var/www/currency_exchange && pip install -r requirments.txt

Run in development mode

    python manage.py runserver