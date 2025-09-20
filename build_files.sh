python3 -m ensurepip --upgrade
pip3 install -r requirements.txt
python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate
python3.14 manage.py collectstatic