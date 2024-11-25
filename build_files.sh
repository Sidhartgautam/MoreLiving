mkdir -p staticfiles
export STATIC_ROOT=staticfiles
pip3 install -r requirements.txt
python3 manage.py collectstatic --noinput